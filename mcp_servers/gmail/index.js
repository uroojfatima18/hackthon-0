import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { google } from "googleapis";
import { readFile } from "fs/promises";
import path from "path";

const TOKEN_PATH = "D:/Urooj/Hackthon 0/token.json";

async function getGmailService() {
  const content = await readFile(TOKEN_PATH, "utf8");
  const credentials = JSON.parse(content);
  
  const auth = new google.auth.OAuth2(
    credentials.client_id,
    credentials.client_secret
  );
  auth.setCredentials(credentials);
  
  return google.gmail({ version: "v1", auth });
}

const server = new Server(
  {
    name: "gmail-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "send_email",
        description: "Send an email via Gmail",
        inputSchema: {
          type: "object",
          properties: {
            to: { type: "string" },
            subject: { type: "string" },
            body: { type: "string" },
          },
          required: ["to", "subject", "body"],
        },
      },
      {
        name: "search_emails",
        description: "Search for emails in Gmail",
        inputSchema: {
          type: "object",
          properties: {
            query: { type: "string", description: "Standard Gmail search query" },
            maxResults: { type: "number", default: 5 },
          },
          required: ["query"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const gmail = await getGmailService();
  
  switch (request.params.name) {
    case "send_email": {
      const { to, subject, body } = request.params.arguments;
      const utf8Subject = `=?utf-8?B?${Buffer.from(subject).toString("base64")}?=`;
      const messageParts = [
        `To: ${to}`,
        "Content-Type: text/plain; charset=utf-8",
        "MIME-Version: 1.0",
        `Subject: ${utf8Subject}`,
        "",
        body,
      ];
      const message = messageParts.join("\n");
      const encodedMessage = Buffer.from(message)
        .toString("base64")
        .replace(/\+/g, "-")
        .replace(/\//g, "_")
        .replace(/=+$/, "");
        
      await gmail.users.messages.send({
        userId: "me",
        requestBody: {
          raw: encodedMessage,
        },
      });
      
      return {
        content: [{ type: "text", text: `✅ Email sent to ${to}` }],
      };
    }
    
    case "search_emails": {
      const { query, maxResults = 5 } = request.params.arguments;
      const res = await gmail.users.messages.list({
        userId: "me",
        q: query,
        maxResults,
      });
      
      const messages = res.data.messages || [];
      const detailedMessages = await Promise.all(
        messages.map(async (m) => {
          const msg = await gmail.users.messages.get({ userId: "me", id: m.id });
          return {
            id: m.id,
            snippet: msg.data.snippet,
            subject: msg.data.payload.headers.find(h => h.name === 'Subject')?.value
          };
        })
      );
      
      return {
        content: [{ type: "text", text: JSON.stringify(detailedMessages, null, 2) }],
      };
    }
    
    default:
      throw new Error(`Unknown tool: ${request.params.name}`);
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Gmail MCP server running...");
