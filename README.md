# Hunter - Email Account Finder

Hunter is a powerful tool that helps you find accounts associated with an email address across various online platforms. It checks for account existence on social media platforms, email providers, shopping websites, gaming platforms, and more.

## Features

- **Multi-Platform Support**: Checks email existence across 100+ platforms
- **Detailed Results**: Provides comprehensive information about found accounts
- **Rate Limit Handling**: Built-in rate limit detection and handling
- **Error Handling**: Robust error handling and reporting
- **Extensible**: Easy to add new platforms and modules

## Supported Platforms

### Social Media
- Facebook
- Twitter
- LinkedIn
- Instagram
- GitHub
- GitLab
- Medium
- Reddit
- Pinterest
- Discord

### Email Providers
- Gmail
- Outlook
- Yahoo
- ProtonMail
- Tutanota

### Shopping
- Amazon
- eBay
- Etsy
- AliExpress
- Shopify

### Gaming
- Steam
- Epic Games
- Battle.net
- Origin
- Uplay

### Professional
- LinkedIn
- Indeed
- Glassdoor
- AngelList
- Behance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/whoamikiddie/hunter.git
cd hunter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python3 -m hunter.core example@gmail.com
```

Options:
- `--no-clear`: Don't clear screen before showing results
- `--timeout`: Set timeout for requests (default: 10 seconds)
- `--threads`: Number of concurrent threads (default: 10)

Example:
```bash
python3 -m hunter.core example@gmail.com --no-clear --timeout 15 --threads 20
```

## Output Format

The tool returns results in JSON format with the following structure:

```json
{
    "name": "platform_name",
    "domain": "platform_domain",
    "method": "detection_method",
    "frequent_rate_limit": true/false,
    "rateLimit": true/false,
    "exists": true/false,
    "emailrecovery": "recovery_email",
    "phoneNumber": "phone_number",
    "others": {
        // Additional platform-specific information
    }
}
```

## Adding New Modules

1. Create a new file in the appropriate directory under `hunter/modules/`
2. Implement the module function with the following signature:
```python
async def platform_name(email, client, out):
    # Your implementation here
```

3. The function should append results to the `out` list in the standard format

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Error Handling

The tool handles various types of errors:
- Rate limiting
- Network issues
- Invalid responses
- Platform-specific errors

Each error is properly reported in the output with appropriate status codes.

## Rate Limiting

The tool implements several strategies to handle rate limiting:
- Automatic retry with exponential backoff
- Request throttling
- Platform-specific rate limit detection
- User-agent rotation

## Security

- No API keys required for basic functionality
- Secure handling of sensitive information
- No data storage or logging
- Respects platform terms of service

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors
- Inspired by various OSINT tools
- Built with Python and asyncio

## Support

For support, please:
1. Check the [Issues](https://github.com/whoamikiddie/hunter/issues) page
2. Create a new issue if needed


## Disclaimer

This tool is for educational purposes only. Users are responsible for complying with the terms of service of each platform they check. The authors are not responsible for any misuse or damage caused by this tool. 