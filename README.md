# Empório da Música — AI-Powered Virtual Assistant

A technical challenge project developed as part of the recruitment process for the **AI Engineer – Full-Stack for Generative AI Applications** position at Artefact.

This project consists of a virtual assistant for the fictional music store Empório da Música, located in Campo Grande, Brazil. It uses a Large Language Model (LLM) with tool-calling capabilities to answer customer questions about products, prices, orders, and store policies.

## Technologies

- **Python 3.12:** Main programming language.
- **LangChain:** Agent creation and tool orchestration.
- **Groq:** LLM inference provider.
- **GPT-OSS 120B:** Language model used by the assistant.
- **Pandas:** CSV data loading and manipulation.
- **pypdf:** PDF text extraction.
- **python-dotenv:** Environment variable management.
- **LangGraph:** Conversation state management through `InMemorySaver`.

## Features

The assistant has four main tools:

### 1. Product Search

Searches the store's product catalog using product names, descriptions, and categories.

The tool returns:
- Product ID.
- Product name and category.
- Description.
- Price.
- Available stock quantity.

### 2. Product Price Lookup

Retrieves product prices and checks applicable commercial conditions.

It considers:
- Original price.
- Active promotions.
- PIX payment discounts.
- Payment conditions documented in the store policies.

Monetary calculations use Python's `Decimal` to avoid common floating-point precision issues.

### 3. Customer Order Lookup

Retrieves customer orders using the customer's identifier (`customer_id`).

Available information includes:
- Order ID.
- Order date and status.
- Total amount.
- Payment method.
- Tracking code.
- Estimated delivery date.
- Associated products.

### 4. Store Policy Search

Extracts and retrieves information from the store's PDF policy document.

Supported topics include:
- Payment methods.
- Shipping and delivery.
- Exchanges and returns.
- Warranty.
- Promotions.
- General store information.

The retrieval mechanism uses lexical matching between query terms and extracted document sections.

## Project Architecture

```text
Desafio_Artefact_DataAI_Engineer/
│
├── data/
│   ├── categories.csv
│   ├── customers.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── products.csv
│   ├── promotions.csv
│   └── políticas_da_loja.pdf
│
├── src/
│   ├── data/
│   │   └── loader.py
│   │
│   ├── tools/
│   │   ├── orders.py
│   │   ├── policies.py
│   │   └── products.py
│   │
│   └── agent.py
│
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

### Module Responsibilities

- `main.py`: Application entry point and terminal-based user interaction.
- `src/agent.py`: LLM configuration, tool definitions, system instructions, and agent creation.
- `src/data/loader.py`: CSV data loading.
- `src/tools/products.py`: Product search and price lookup tools.
- `src/tools/orders.py`: Customer order lookup tool.
- `src/tools/policies.py`: PDF extraction and policy retrieval tool.

## Installation and Configuration

### Prerequisites

- Python 3.12 or later.
- Git.
- A Groq API key.

### 1. Clone the repository

```bash
git clone <REPOSITORY_URL>
cd Desafio_Artefact_DataAI_Engineer
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a copy of `.env.example` named `.env`.

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Add your Groq API key to the `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

You can obtain an API key from the [Groq Console](https://console.groq.com/).

**Important:** Never commit or share your `.env` file or API key.

## Running the Application

With the virtual environment activated and dependencies installed, run:

```bash
py main.py
```

The assistant will start an interactive terminal session.

To end the conversation, type:

```text
sair
```

## Example Interaction Scenarios

The following scenarios illustrate the main capabilities tested during development:

### 1. Product Search

**User:**

Which Yamaha acoustic guitars are currently available?

**Expected behavior:**

The assistant searches the product catalog and presents matching products with their names, prices, and available stock quantities.

### 2. Product Price Lookup

**User:**

How much does the Yamaha C40 Nylon Natural cost when paying with PIX?

**Expected behavior:**

The assistant retrieves the original price, calculates the applicable PIX discount, and presents the final price.

### 3. Customer Order Lookup

**User:**

Can you check my order? My customer ID is 1.

**Expected behavior:**

The assistant retrieves the customer's order information, including its status, total amount, tracking code, and associated products.

### 4. Store Policy Search

**User:**

How does delivery work for customers in the Campo Grande metropolitan area? Is free shipping available?

**Expected behavior:**

The assistant retrieves the relevant delivery policy and explains the free-shipping threshold, fixed delivery fee, and estimated delivery time.

## Technical Decisions

- **Separation of responsibilities:** Tools are organized into independent modules to improve maintainability and facilitate future development.
- **Centralized data loading:** CSV files are loaded during application initialization and shared across the tools.
- **Tool calling:** The agent uses external tools to retrieve structured business data and store policies instead of relying exclusively on the LLM's internal knowledge.
- **Monetary precision:** `Decimal` is used for price and discount calculations.
- **Conversation memory:** `InMemorySaver` is used to preserve conversation state during the application session.
- **System instructions:** The system prompt establishes behavioral rules to reduce unsupported answers and prevent the generation of undocumented commercial information.
- **Policy retrieval:** A lexical matching strategy was chosen to retrieve relevant sections from the PDF without introducing the additional infrastructure required by an embedding-based retrieval system.

## Known Limitations and Future Improvements

- **Synthetic data:** The application uses fictional store data provided for the technical challenge.
- **Customer authentication:** Order lookup relies on `customer_id` and does not implement identity verification. A production application would require an authentication mechanism.
- **Conversation persistence:** Conversation state is stored in memory and is lost when the application terminates. Persistent storage could be implemented in a future version.
- **Policy retrieval:** The current implementation uses lexical matching rather than semantic search with embeddings. A more advanced retrieval strategy could improve results for queries with different wording.
- **External API dependency:** The application depends on Groq API availability and is subject to the provider's usage limits.
- **Limited business operations:** The assistant does not execute purchases, process payments, modify orders, or reserve products.

With additional development time, improvements could include automated tests, stronger customer authentication, persistent conversation storage, semantic document retrieval, and a web-based interface.

## AI Assistance and Development Workflow

AI-powered tools were used as development assistants throughout this project:

- **GitHub Copilot:** Used to assist with coding, implementation suggestions, and troubleshooting during development.
- **ChatGPT:** Used to help understand technical concepts, analyze code, troubleshoot implementation issues, organize project documentation, and prepare this README.

These tools supported the development process. Implementation decisions, component integration, validation, and application testing were conducted throughout the technical challenge.

The virtual assistant itself uses **GPT-OSS 120B**, accessed through Groq, to interpret user requests and determine when to invoke its available tools.

---

**Developed for the Artefact 2026 Technical Challenge.**