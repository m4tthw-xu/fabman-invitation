# Texas Inventionworks Fabman Invitation App

A web application that allows searching and sending invitations to Fabman members. Built with Flask and the Fabman API and deployed on AWS Elastic Beanstalk.

## Features

- Search Fabman members by name or eid
- Send invitations to members directly
- Dark/Light theme toggle

## Prerequisites

- Python 3.12+
- AWS account with access to TIW Secrets Manager and Elastic Beanstalk

## Installation

1. Clone the repository:
git clone <repository-url>
cd <repository-name>

2. Create and activate a virtual environment:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Set up environment variables:
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key

## Local Development

Run the Flask development server:
python application.py

The application will be available at http://localhost:5000

## Deployment

The application is configured for AWS Elastic Beanstalk deployment.

1. Initialize Elastic Beanstalk (first time only):
eb init

2. Create an environment (first time only):
eb create fabman-search-env

3. Deploy updates:
eb deploy

## API Endpoints

### GET /api/search-members
Search for Fabman members.

Query Parameters:
- q: Search term (required)

Response:
{
    "success": true,
    "members": [
        {
            "id": "123",
            "name": "John Doe",
            "email": "john@example.com"
        }
    ]
}

### POST /api/send-invitation/{member_id}
Send an invitation to a specific member.

Response:
{
    "success": true,
    "message": "Invitation sent successfully to member 123"
}

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.