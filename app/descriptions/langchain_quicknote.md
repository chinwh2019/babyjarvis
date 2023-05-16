# Blog Post: Understanding LangChain, LangChain Agent, and LangChain Memory

## Introduction to LangChain

In the evolving world of artificial intelligence and language processing, LangChain stands as a novel framework designed for developing applications powered by language models. The core belief behind LangChain is that the most powerful and differentiated applications should not only interact with a language model via an API but also be data-aware and agentic.

Being data-aware means connecting a language model to other sources of data, providing a broader context and richer responses. Being agentic, on the other hand, allows a language model to interact with its environment autonomously, making decisions based on its understanding and objectives.

## What is a LangChain Agent?

Within the LangChain framework, an Agent acts as a wrapper around a language model. It is designed to accept user input and return a response corresponding to an action to take, along with a corresponding action input. The purpose of an Agent is to facilitate interaction between the language model and the environment, allowing the model to perceive its environment, make decisions, and take actions to achieve specific goals. This design enables the Agent to operate autonomously without direct human control, thereby extending the functionality of the underlying language model.

## LangChain Memory: Remembering Interactions

LangChain introduces the concept of 'Memory', which is a significant component of the framework. By default, LangChain's Chains and Agents are stateless, treating each incoming query independently. However, in certain applications, such as chatbots, it is crucial to remember previous interactions at both a short-term and long-term level. That's where Memory comes into play.

LangChain provides Memory components in two forms. Firstly, it offers helper utilities for managing and manipulating previous chat messages, designed to be modular and useful regardless of how they are used. Secondly, LangChain provides easy ways to incorporate these utilities into Chains, extending the functionalities of the system.

With Memory, LangChain enhances the experience and effectiveness of language model applications by allowing them to remember and reference previous interactions. This feature brings the system closer to a more human-like interaction model, where context from previous discussions informs the current conversation.

## Wrap up

Memory in Langchain:

- How to Add Memory to an Agent:

1. Create an LLMChain with memory.
2. Use the LLMchain to create a custom Agent.

- How to Add Memory to a Chain:

1. Setup Prompt and Memory
2. Intialize LLMChain
3. Call the LLMChain

- Vector Store-backed Memory:

1. Stores memories in a VectorDB
2. Queries the top-K most relevant docs
3. Pros:
    - Does not explicity track the order of messages
    - AI can remember relevant pieces of information that it was told earlier

- ConversationBufferMemory:

1. Memory allows for storing of messages
2. Extracts the messages in a variable
3. Pros:
    - Basic to understand/pick up

- ConversationBufferWindowMemory:

1. Only uses the last K messages
2. Pros:
    - Useful to keep the memory history small

- ConversationSummaryMemory:

1. Creates a summary of the conversation over time.
2. Pros:
    - Useful for summarizing the conversation over time

## Conclusion

LangChain, with its Agent and Memory components, is a promising framework that enriches language model applications. By allowing language models to connect with other data sources, interact with their environment, and remember previous interactions, LangChain pushes the boundaries of what language model applications can achieve, making them more powerful and user-friendly. As the field of artificial intelligence continues to evolve, it will be exciting to see how frameworks like LangChain will shape the future of language model applications.
