# Abdul Store - Pakistan Number Info API

A high-performance Pakistan Number Information API designed for Cloudflare Workers. 

## Features
- **Cloudflare Native**: Built with Hono and optimized for Cloudflare Workers.
- **Fast**: Minimal latency with edge computing.
- **JSON Support**: Returns all data in clean, structured JSON format.
- **CORS Enabled**: Can be called from any frontend.

## API Endpoints

### 1. Home
- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns API status and usage information.

### 2. Search Number
- **URL**: `/api?num=3359736848`
- **Method**: `GET`
- **Parameters**: `num` (Required) - The mobile number to search.
- **Response**:
```json
{
  "success": true,
  "count": 1,
  "results": [
    {
      "number": "3359736848",
      "name": "NAME",
      "cnic": "CNIC",
      "address": "ADDRESS"
    }
  ]
}
```

## Local Development
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start development server:
   ```bash
   npm run dev
   ```

## Deployment
To deploy to Cloudflare:
```bash
npm run deploy
```

## Credits
Author: OGAbdulOfficial
