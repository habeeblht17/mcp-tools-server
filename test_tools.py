"""
Simple test script to verify all MCP tools are working correctly
Run this after setting up your .env file with API keys

Usage: python test_tools.py
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_test_result(tool_name, result):
    """Print formatted test result"""
    print(f"\n{'='*60}")
    print(f"Testing: {tool_name}")
    print(f"{'='*60}")
    print(f"Result: {result}")
    print(f"Status: {'✓ PASSED' if result.get('status') == 'success' else '✗ FAILED'}")

# ============================================================================
# Copy of tool functions without @mcp.tool() decorator for testing
# ============================================================================

def get_weather(location: str) -> dict:
    """Retrieve current weather conditions for any city or location."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return {
            "error": "OpenWeather API key not configured. Please add OPENWEATHER_API_KEY to .env file",
            "status": "error"
        }
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "location": data["name"],
            "country": data["sys"]["country"],
            "temperature": f"{data['main']['temp']}°C",
            "feels_like": f"{data['main']['feels_like']}°C",
            "description": data["weather"][0]["description"].title(),
            "humidity": f"{data['main']['humidity']}%",
            "wind_speed": f"{data['wind']['speed']} m/s",
            "status": "success"
        }
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": f"Location '{location}' not found", "status": "error"}
        return {"error": f"API error: {str(e)}", "status": "error"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}", "status": "error"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "status": "error"}


def calculate(operation: str, num1: float, num2: float) -> dict:
    """Perform basic arithmetic operations."""
    try:
        operations = {
            "add": lambda a, b: a + b,
            "subtract": lambda a, b: a - b,
            "multiply": lambda a, b: a * b,
            "divide": lambda a, b: a / b if b != 0 else None
        }
        
        operation = operation.lower()
        
        if operation not in operations:
            return {
                "error": f"Invalid operation '{operation}'. Use: add, subtract, multiply, divide",
                "status": "error"
            }
        
        result = operations[operation](num1, num2)
        
        if result is None:
            return {
                "error": "Cannot divide by zero",
                "status": "error"
            }
        
        return {
            "operation": operation,
            "num1": num1,
            "num2": num2,
            "result": result,
            "expression": f"{num1} {operation} {num2} = {result}",
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"Calculation error: {str(e)}", "status": "error"}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert amount between different currencies using live exchange rates."""
    api_key = os.getenv("EXCHANGERATE_API_KEY")
    
    if not api_key:
        return {
            "error": "ExchangeRate API key not configured. Please add EXCHANGERATE_API_KEY to .env file",
            "status": "error"
        }
    
    try:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data["result"] == "error":
            return {
                "error": f"Currency conversion error: {data.get('error-type', 'Unknown error')}",
                "status": "error"
            }
        
        return {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "conversion_rate": data["conversion_rate"],
            "converted_amount": data["conversion_result"],
            "formatted": f"{amount} {from_currency} = {data['conversion_result']:.2f} {to_currency}",
            "last_updated": data.get("time_last_update_utc", "N/A"),
            "status": "success"
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}", "status": "error"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "status": "error"}


def get_timezone_info(city: str) -> dict:
    """Get current time and timezone information for a given city."""
    try:
        # City to timezone and UTC offset mapping
        city_data = {
            "london": {"timezone": "Europe/London", "offset": "+00:00"},
            "paris": {"timezone": "Europe/Paris", "offset": "+01:00"},
            "new york": {"timezone": "America/New_York", "offset": "-05:00"},
            "los angeles": {"timezone": "America/Los_Angeles", "offset": "-08:00"},
            "tokyo": {"timezone": "Asia/Tokyo", "offset": "+09:00"},
            "sydney": {"timezone": "Australia/Sydney", "offset": "+11:00"},
            "dubai": {"timezone": "Asia/Dubai", "offset": "+04:00"},
            "singapore": {"timezone": "Asia/Singapore", "offset": "+08:00"},
            "mumbai": {"timezone": "Asia/Kolkata", "offset": "+05:30"},
            "toronto": {"timezone": "America/Toronto", "offset": "-05:00"},
            "berlin": {"timezone": "Europe/Berlin", "offset": "+01:00"},
            "moscow": {"timezone": "Europe/Moscow", "offset": "+03:00"},
            "beijing": {"timezone": "Asia/Shanghai", "offset": "+08:00"},
            "hong kong": {"timezone": "Asia/Hong_Kong", "offset": "+08:00"},
            "chicago": {"timezone": "America/Chicago", "offset": "-06:00"},
            "mexico city": {"timezone": "America/Mexico_City", "offset": "-06:00"},
            "sao paulo": {"timezone": "America/Sao_Paulo", "offset": "-03:00"},
            "cairo": {"timezone": "Africa/Cairo", "offset": "+02:00"},
            "lagos": {"timezone": "Africa/Lagos", "offset": "+01:00"},
            "johannesburg": {"timezone": "Africa/Johannesburg", "offset": "+02:00"}
        }
        
        city_lower = city.lower().strip()
        city_info = city_data.get(city_lower)
        
        if not city_info:
            return {
                "error": f"City '{city}' not found in database. Supported cities: {', '.join(city_data.keys())}",
                "status": "error"
            }
        
        # Try WorldTimeAPI first (most accurate)
        try:
            url = f"http://worldtimeapi.org/api/timezone/{city_info['timezone']}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            dt = datetime.fromisoformat(data["datetime"].replace("Z", "+00:00"))
            
            return {
                "city": city.title(),
                "timezone": data["timezone"],
                "current_time": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "utc_offset": data["utc_offset"],
                "day_of_week": dt.strftime("%A"),
                "day_of_year": data["day_of_year"],
                "week_number": data["week_number"],
                "status": "success"
            }
        except:
            # Fallback: Calculate time using UTC offset
            from datetime import timezone, timedelta
            
            # Parse offset like "+09:00" or "-05:00"
            offset_str = city_info['offset']
            sign = 1 if offset_str[0] == '+' else -1
            hours, minutes = map(int, offset_str[1:].split(':'))
            offset = timedelta(hours=sign*hours, minutes=sign*minutes)
            
            # Get current UTC time and apply offset
            utc_now = datetime.now(timezone.utc)
            local_time = utc_now + offset
            
            return {
                "city": city.title(),
                "timezone": city_info['timezone'],
                "current_time": local_time.strftime("%Y-%m-%d %H:%M:%S"),
                "utc_offset": offset_str,
                "day_of_week": local_time.strftime("%A"),
                "day_of_year": local_time.timetuple().tm_yday,
                "week_number": local_time.isocalendar()[1],
                "note": "Using calculated time (WorldTimeAPI unavailable)",
                "status": "success"
            }
        
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "status": "error"}


def convert_units(value: float, from_unit: str, to_unit: str, category: str) -> dict:
    """Convert between common units of measurement."""
    try:
        category = category.lower()
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        length_units = {
            "meters": 1, "m": 1,
            "kilometers": 1000, "km": 1000,
            "miles": 1609.34,
            "feet": 0.3048, "ft": 0.3048,
            "inches": 0.0254, "in": 0.0254,
            "yards": 0.9144, "yd": 0.9144,
            "centimeters": 0.01, "cm": 0.01,
            "millimeters": 0.001, "mm": 0.001
        }
        
        weight_units = {
            "kilograms": 1, "kg": 1,
            "grams": 0.001, "g": 0.001,
            "pounds": 0.453592, "lbs": 0.453592,
            "ounces": 0.0283495, "oz": 0.0283495,
            "tons": 1000, "tonnes": 1000
        }
        
        if category == "length":
            if from_unit not in length_units or to_unit not in length_units:
                return {
                    "error": f"Invalid length units. Supported: {', '.join(set(length_units.keys()))}",
                    "status": "error"
                }
            
            meters = value * length_units[from_unit]
            result = meters / length_units[to_unit]
            
        elif category == "weight":
            if from_unit not in weight_units or to_unit not in weight_units:
                return {
                    "error": f"Invalid weight units. Supported: {', '.join(set(weight_units.keys()))}",
                    "status": "error"
                }
            
            kg = value * weight_units[from_unit]
            result = kg / weight_units[to_unit]
            
        elif category == "temperature":
            if from_unit == "celsius" and to_unit == "fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                result = (value - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "kelvin":
                result = value + 273.15
            elif from_unit == "kelvin" and to_unit == "celsius":
                result = value - 273.15
            elif from_unit == "fahrenheit" and to_unit == "kelvin":
                result = (value - 32) * 5/9 + 273.15
            elif from_unit == "kelvin" and to_unit == "fahrenheit":
                result = (value - 273.15) * 9/5 + 32
            elif from_unit == to_unit:
                result = value
            else:
                return {
                    "error": "Invalid temperature units. Supported: celsius, fahrenheit, kelvin",
                    "status": "error"
                }
        else:
            return {
                "error": f"Invalid category '{category}'. Use: length, weight, temperature",
                "status": "error"
            }
        
        return {
            "value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "category": category,
            "result": round(result, 4),
            "formatted": f"{value} {from_unit} = {round(result, 4)} {to_unit}",
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"Conversion error: {str(e)}", "status": "error"}


# ============================================================================
# TEST RUNNER
# ============================================================================

def run_tests():
    """Run tests for all tools"""
    print("\n🧪 MCP Tools Server - Test Suite")
    print("="*60)
    
    # Test 1: Weather Tool
    print("\n1️⃣ Testing Weather Tool...")
    weather_result = get_weather("London")
    print_test_result("Weather Tool (London)", weather_result)
    
    # Test 2: Calculator Tool
    print("\n2️⃣ Testing Calculator Tool...")
    calc_result = calculate("multiply", 15, 4)
    print_test_result("Calculator Tool (15 × 4)", calc_result)
    
    # Test division by zero handling (should return error)
    print("\n   Testing Error Handling (Division by Zero)...")
    calc_error = calculate("divide", 10, 0)
    print(f"   Result: {calc_error}")
    print(f"   Status: {'✓ PASSED (Error handled correctly)' if calc_error.get('status') == 'error' else '✗ FAILED'}")
    
    # Test 3: Currency Converter Tool
    print("\n3️⃣ Testing Currency Converter Tool...")
    currency_result = convert_currency(100, "USD", "EUR")
    print_test_result("Currency Converter (100 USD to EUR)", currency_result)
    
    # Test 4: Time Zone Tool
    print("\n4️⃣ Testing Time Zone Tool...")
    timezone_result = get_timezone_info("Tokyo")
    print_test_result("Time Zone Tool (Tokyo)", timezone_result)
    
    # Test 5: Unit Converter Tool
    print("\n5️⃣ Testing Unit Converter Tool...")
    
    # Test length conversion
    length_result = convert_units(100, "km", "miles", "length")
    print_test_result("Unit Converter (100 km to miles)", length_result)
    
    # Test weight conversion
    weight_result = convert_units(75, "kg", "lbs", "weight")
    print_test_result("Unit Converter (75 kg to lbs)", weight_result)
    
    # Test temperature conversion
    temp_result = convert_units(32, "fahrenheit", "celsius", "temperature")
    print_test_result("Unit Converter (32°F to °C)", temp_result)
    
    # Summary
    print("\n" + "="*60)
    print("✅ Test Suite Complete!")
    print("="*60)
    print("\nIf all tests show 'PASSED', your MCP server is ready!")
    print("If any tests show 'FAILED', check:")
    print("  1. Your .env file has valid API keys")
    print("  2. You have internet connectivity")
    print("  3. The error messages for specific issues")

if __name__ == "__main__":
    # Check if API keys are configured
    if not os.getenv("OPENWEATHER_API_KEY") or not os.getenv("EXCHANGERATE_API_KEY"):
        print("\n⚠️  WARNING: API keys not found in .env file")
        print("Some tests will fail. Please configure your .env file first.\n")
    
    run_tests()