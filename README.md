# MCP Tools Server

A Model Context Protocol (MCP) server providing 5 essential tools for weather information, calculations, currency conversion, timezone queries, and unit conversions.

Built with Python and FastMCP for AI Engineering applications.

## 🚀 Features

This MCP server provides the following tools:

### 1. Weather Tool
Retrieve current weather conditions for any city or location worldwide.
- Supports city names, ZIP codes, and "City,Country" format
- Returns temperature, humidity, wind speed, and weather description
- Uses OpenWeatherMap API

### 2. Calculator Tool
Perform basic arithmetic operations with proper error handling.
- Operations: addition, subtraction, multiplication, division
- Handles division by zero gracefully
- Returns formatted expressions

### 3. Currency Converter Tool
Convert amounts between different currencies using live exchange rates.
- Supports 150+ currencies
- Real-time exchange rates
- Uses ExchangeRate-API

### 4. Time Zone Tool
Get current time and timezone information for major cities.
- Supports 20+ major cities worldwide
- Returns current time, UTC offset, day of week
- Uses WorldTimeAPI (no API key required)

### 5. Unit Converter Tool
Convert between common units of measurement.
- **Length**: meters, kilometers, miles, feet, inches, yards, centimeters, millimeters
- **Weight**: kilograms, grams, pounds, ounces, tons
- **Temperature**: Celsius, Fahrenheit, Kelvin

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- API keys for:
  - [OpenWeatherMap](https://openweathermap.org/api) (free tier)
  - [ExchangeRate-API](https://www.exchangerate-api.com/) (free tier)

## 🛠️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/mcp-tools-server.git
cd mcp-tools-server
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# On Windows Command Prompt:
.\venv\Scripts\activate.bat

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   OPENWEATHER_API_KEY=your_actual_api_key_here
   EXCHANGERATE_API_KEY=your_actual_api_key_here
   ```

## 🚀 Usage

### Running the Server

```bash
python server.py
```

The server will start and be available for MCP client connections.

### Connecting with Claude Desktop

1. Open your Claude Desktop configuration file:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Add the server configuration:
   ```json
   {
     "mcpServers": {
       "tools-server": {
         "command": "python",
         "args": ["C:/path/to/your/mcp-tools-server/server.py"],
         "env": {}
       }
     }
   }
   ```

3. Restart Claude Desktop

### Using MCP Inspector

```bash
# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# Run inspector with your server
mcp-inspector python server.py
```

## 📖 Tool Documentation

### Weather Tool

**Function**: `get_weather(location: str)`

**Description**: Retrieves current weather conditions for a specified location.

**Parameters**:
- `location` (string): City name, ZIP code, or "City,Country" format

**Example Request**:
```json
{
  "tool": "get_weather",
  "arguments": {
    "location": "London"
  }
}
```

**Example Response**:
```json
{
  "location": "London",
  "country": "GB",
  "temperature": "12°C",
  "feels_like": "10°C",
  "description": "Scattered Clouds",
  "humidity": "76%",
  "wind_speed": "4.5 m/s",
  "status": "success"
}
```

---

### Calculator Tool

**Function**: `calculate(operation: str, num1: float, num2: float)`

**Description**: Performs basic arithmetic operations.

**Parameters**:
- `operation` (string): One of "add", "subtract", "multiply", "divide"
- `num1` (float): First number
- `num2` (float): Second number

**Example Request**:
```json
{
  "tool": "calculate",
  "arguments": {
    "operation": "multiply",
    "num1": 15,
    "num2": 4
  }
}
```

**Example Response**:
```json
{
  "operation": "multiply",
  "num1": 15,
  "num2": 4,
  "result": 60,
  "expression": "15 multiply 4 = 60",
  "status": "success"
}
```

---

### Currency Converter Tool

**Function**: `convert_currency(amount: float, from_currency: str, to_currency: str)`

**Description**: Converts an amount from one currency to another using live exchange rates.

**Parameters**:
- `amount` (float): Amount to convert
- `from_currency` (string): Source currency code (e.g., "USD", "EUR")
- `to_currency` (string): Target currency code

**Example Request**:
```json
{
  "tool": "convert_currency",
  "arguments": {
    "amount": 100,
    "from_currency": "USD",
    "to_currency": "EUR"
  }
}
```

**Example Response**:
```json
{
  "amount": 100,
  "from_currency": "USD",
  "to_currency": "EUR",
  "conversion_rate": 0.92,
  "converted_amount": 92.0,
  "formatted": "100 USD = 92.00 EUR",
  "last_updated": "Wed, 08 Jan 2025 00:00:01 +0000",
  "status": "success"
}
```

---

### Time Zone Tool

**Function**: `get_timezone_info(city: str)`

**Description**: Gets current time and timezone information for a given city.

**Parameters**:
- `city` (string): City name (e.g., "Tokyo", "New York")

**Supported Cities**: London, Paris, New York, Los Angeles, Tokyo, Sydney, Dubai, Singapore, Mumbai, Toronto, Berlin, Moscow, Beijing, Hong Kong, Chicago, Mexico City, Sao Paulo, Cairo, Lagos, Johannesburg

**Example Request**:
```json
{
  "tool": "get_timezone_info",
  "arguments": {
    "city": "Tokyo"
  }
}
```

**Example Response**:
```json
{
  "city": "Tokyo",
  "timezone": "Asia/Tokyo",
  "current_time": "2026-01-10 15:30:45",
  "utc_offset": "+09:00",
  "day_of_week": "Saturday",
  "day_of_year": 10,
  "week_number": 2,
  "status": "success"
}
```

---

### Unit Converter Tool

**Function**: `convert_units(value: float, from_unit: str, to_unit: str, category: str)`

**Description**: Converts between common units of measurement.

**Parameters**:
- `value` (float): Numeric value to convert
- `from_unit` (string): Source unit
- `to_unit` (string): Target unit
- `category` (string): One of "length", "weight", "temperature"

**Example Request (Length)**:
```json
{
  "tool": "convert_units",
  "arguments": {
    "value": 100,
    "from_unit": "km",
    "to_unit": "miles",
    "category": "length"
  }
}
```

**Example Response**:
```json
{
  "value": 100,
  "from_unit": "km",
  "to_unit": "miles",
  "category": "length",
  "result": 62.1371,
  "formatted": "100 km = 62.1371 miles",
  "status": "success"
}
```

**Example Request (Temperature)**:
```json
{
  "tool": "convert_units",
  "arguments": {
    "value": 32,
    "from_unit": "fahrenheit",
    "to_unit": "celsius",
    "category": "temperature"
  }
}
```

**Example Response**:
```json
{
  "value": 32,
  "from_unit": "fahrenheit",
  "to_unit": "celsius",
  "category": "temperature",
  "result": 0.0,
  "formatted": "32 fahrenheit = 0.0 celsius",
  "status": "success"
}
```

## 🧪 Testing

### Manual Testing with MCP Inspector

1. Install MCP Inspector:
   ```bash
   npm install -g @modelcontextprotocol/inspector
   ```

2. Run the inspector:
   ```bash
   mcp-inspector python server.py
   ```

3. Test each tool through the inspector interface

### Testing with Claude Desktop

1. Configure Claude Desktop (see Usage section)
2. In a conversation, ask Claude to use the tools:
   - "What's the weather in Paris?"
   - "Convert 100 USD to EUR"
   - "What time is it in Tokyo?"
   - "Calculate 25 multiplied by 4"
   - "Convert 100 kilometers to miles"

## 📁 Project Structure

```
mcp-tools-server/
│
├── server.py              # Main MCP server implementation
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys) - not in git
├── .env.example          # Example environment file
├── .gitignore            # Git ignore file
├── README.md             # This file
└── venv/                 # Virtual environment (not in git)
```

## 🔒 Security Notes

- Never commit your `.env` file to Git
- The `.gitignore` file is configured to exclude sensitive files
- API keys are stored securely in environment variables
- All API requests include timeout protection

## 🐛 Error Handling

All tools include comprehensive error handling for:
- Invalid inputs
- Missing API keys
- Network failures
- API errors
- Division by zero (calculator)
- Invalid currency codes
- Unknown cities/locations

Errors are returned in a consistent format:
```json
{
  "error": "Descriptive error message",
  "status": "error"
}
```

## 📝 Dependencies

- `fastmcp` - FastMCP framework for building MCP servers
- `requests` - HTTP library for API calls
- `python-dotenv` - Environment variable management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Your Name - Habeeb Temitope Lawal

## 🙏 Acknowledgments

- FastMCP framework
- OpenWeatherMap API
- ExchangeRate-API
- WorldTimeAPI