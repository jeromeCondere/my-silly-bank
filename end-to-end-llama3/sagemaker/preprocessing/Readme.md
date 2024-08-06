# Scenario-Based Conversation Generator

This Python script creates simulated conversations for various simple financial requests. Each **scenario** is a sequence of **questions and answers** that are automatically generated using predefined functions. These conversations cover a range of topics, like checking transactions, viewing balances, withdrawing money, and more.

## How It Works:

### 1. Scenario Creation
Each **scenario** includes a set of steps, like asking to see transaction history or checking the balance. The script puts these steps together based to create specific use cases.

### 2. Questions & Answers
The script uses functions to randomly pick questions and answers. For example, if a user wants to see their last few transactions, the script might randomly choose a question like "Can I see my most recent transactions?" and follow it with a response like "Here’s your transaction history: ###Transactions."

### 3. Other Financial Actions
The script can handle lots of different actions, like:
- **Deposits**: Asking about depositing money.
- **Withdrawals**: Making a withdrawal request.
- **Balance**: Checking the account balance.
- **Stocks**: Asking about stock holdings.
- **Buying Stocks**: Buying stocks or investments.

## Generating Training Data

The `generate_training_data` function creates the training data by combining random names, companies, and amounts. It then generates conversations based on different scenarios (like checking balances, withdrawing funds, or buying stocks) and writes these to a CSV file. Each conversation is saved as a row with a JSON version of the interactions, so it’s ready to use for training or testing AI models.

## Example Conversations
- **Scenario 1**: Greeting → Request to check balance → Display balance.
- **Scenario 2**: Request for stock information → Response with stock details → Displaying stocks.
- **Scenario 3**: Greeting → Request to withdraw funds → Withdrawal response.
- And more...

## Usage
To generate training data, simply call the `generate_training_data` function with your desired parameters, such as the filename to save the data, and the number of names and companies to include. This will produce a CSV file with simulated conversation data.

