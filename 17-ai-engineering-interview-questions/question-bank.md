# AI Engineering Interview Question Bank

This is the consolidated final revision bank from the Notion Interview Preparation plan.

## 1. Python & Software Engineering

1. What is the difference between a list, tuple, set, and dictionary in Python?
2. What are Python generators and when would you use them?
3. Explain iterators versus iterables.
4. What is the difference between shallow copy and deep copy?
5. Explain mutable versus immutable objects.
6. What are decorators and where are they useful in AI services?
7. How does Python garbage collection work?
8. What are context managers and how would you implement one?
9. What is the difference between multiprocessing, multithreading, and asyncio?
10. How does the GIL affect CPU-bound and I/O-bound workloads?
11. How would you profile a slow Python program?
12. Explain Big-O time and space complexity with examples.
13. Implement binary search and explain its complexity.
14. How would you find duplicates efficiently in a large list?
15. How would you design testable Python code?

## 2. Mathematics & Statistics

1. What is a vector, matrix, and tensor?
2. Explain dot product and cosine similarity.
3. What is a derivative and why is it important in machine learning?
4. Explain partial derivatives and gradients.
5. What is the chain rule and why is it central to backpropagation?
6. Explain gradient descent mathematically.
7. What is the difference between batch, stochastic, and mini-batch gradient descent?
8. What is variance and why does it matter?
9. Explain covariance and correlation.
10. What are probability distributions and why do ML models use them?
11. Explain Bayes' theorem.
12. What is maximum likelihood estimation?
13. What is entropy?
14. What is cross-entropy loss?
15. Explain expectation and conditional probability.

## 3. Machine Learning Fundamentals

1. What is supervised versus unsupervised learning?
2. Explain train, validation, and test sets.
3. What is overfitting and how do you detect it?
4. What is underfitting?
5. Explain bias-variance trade-off.
6. What is regularization and why does it help?
7. Compare L1 and L2 regularization.
8. How does logistic regression work?
9. Explain decision trees and random forests.
10. What is boosting?
11. Compare bagging and boosting.
12. How do you handle class imbalance?
13. Precision versus recall—which matters for fraud detection and why?
14. Explain ROC-AUC and PR-AUC.
15. How would you select features for a model?
16. What is data leakage? Give an example.
17. How would you build a reproducible ML training pipeline?

## 4. Deep Learning

1. What is a neural network?
2. Explain forward propagation and backpropagation.
3. What causes vanishing and exploding gradients?
4. Compare ReLU, sigmoid, and tanh.
5. Why is initialization important?
6. Explain Xavier and He initialization.
7. What is batch normalization?
8. What is dropout?
9. Compare SGD, Adam, and AdamW.
10. What is a learning-rate scheduler?
11. How do CNNs exploit spatial structure?
12. What is pooling?
13. When would you use an RNN, LSTM, or GRU?
14. Why did Transformers largely replace recurrent architectures for many language tasks?
15. How would you debug a neural network whose loss is not decreasing?

## 5. Transformers & LLMs

1. Explain the Transformer architecture from input tokens to output logits.
2. What is self-attention?
3. Why do we divide attention scores by sqrt(d_k)?
4. Explain Query, Key, and Value.
5. What is multi-head attention?
6. Why do Transformers need positional information?
7. Compare encoder-only, decoder-only, and encoder-decoder architectures.
8. Why are decoder-only models effective for text generation?
9. What is causal masking?
10. What is a token embedding?
11. What is next-token prediction?
12. What is pretraining?
13. What is instruction tuning?
14. Explain context window limitations.
15. What causes LLM hallucinations?
16. Explain temperature, top-k, and top-p.
17. What are scaling laws?
18. What are the major Transformer inference bottlenecks?

## 6. LLM Application Engineering

1. How would you choose an LLM for a production application?
2. When would you use prompting instead of fine-tuning?
3. When would you use RAG instead of fine-tuning?
4. How would you design a robust prompt template?
5. What is few-shot prompting?
6. How do you defend against prompt injection?
7. How would you force an LLM to return structured JSON?
8. Why should structured outputs still be validated server-side?
9. Explain tool/function calling.
10. How would you authorize tools safely?
11. What is time-to-first-token (TTFT)?
12. How would you stream an LLM response to a client?
13. How would you implement retries with exponential backoff?
14. Why can retries make an outage worse?
15. How would you implement rate limiting for an AI API?
16. How would you reduce LLM latency?
17. How would you reduce LLM cost?
18. How would you design model fallback and routing?
19. How would you protect PII in prompts and logs?
20. What metrics would you monitor for a production LLM API?

## 7. RAG & Retrieval

1. Explain the complete RAG pipeline.
2. Why does chunking matter?
3. Compare fixed-size, recursive, semantic, and structure-aware chunking.
4. What makes a good chunk size?
5. What are embeddings?
6. Explain cosine similarity.
7. What is a vector database?
8. Compare approximate nearest-neighbor search with brute-force search.
9. What is metadata filtering?
10. Explain hybrid search.
11. Why combine keyword and vector search?
12. What is reranking?
13. What is query rewriting?
14. What is multi-query retrieval?
15. What is context compression?
16. How would you evaluate retrieval quality?
17. Explain Recall@K, Precision@K, MRR, and NDCG.
18. What causes irrelevant retrieval results?
19. What causes missing relevant documents?
20. How would you debug a RAG system producing hallucinated answers?
21. How would you design production RAG for millions of documents?

## 8. Agents & Agentic Systems

1. What is an AI agent?
2. How is an agent different from a deterministic workflow?
3. Explain the ReAct pattern.
4. What is an agent reasoning loop?
5. How should agent state be represented?
6. What belongs in short-term versus long-term memory?
7. How would you prevent an agent from looping forever?
8. How would you enforce a maximum tool-call budget?
9. How do you validate tool inputs and outputs?
10. What is human-in-the-loop execution?
11. When would you use multiple agents?
12. What are the disadvantages of multi-agent architectures?
13. Explain MCP and why standardized tool interfaces matter.
14. How would you evaluate an autonomous agent?
15. What are common agent failure modes?
16. How would you secure an agent that can execute real-world actions?

## 9. Fine-Tuning & Model Adaptation

1. When should you fine-tune a model?
2. Compare prompting, RAG, and fine-tuning.
3. What is supervised fine-tuning?
4. What makes a high-quality fine-tuning dataset?
5. What is PEFT?
6. Explain LoRA mathematically.
7. What is QLoRA?
8. What is quantization?
9. Compare FP32, FP16, BF16, INT8, and INT4.
10. What is catastrophic forgetting?
11. What is preference tuning?
12. Explain RLHF.
13. Explain DPO.
14. How would you evaluate a fine-tuned model?
15. How do you detect overfitting during fine-tuning?
16. How would you deploy adapters separately from the base model?

## 10. AI Infrastructure & Inference

1. Why are GPUs useful for neural-network inference?
2. What determines GPU memory usage?
3. Estimate memory required for a 7B parameter model in FP16.
4. What is batching?
5. Compare static and dynamic batching.
6. What is KV caching?
7. Why does KV cache increase memory usage?
8. What is continuous batching?
9. Compare latency and throughput.
10. What is a model-serving system?
11. What problems do inference servers such as vLLM solve?
12. What is tensor parallelism?
13. What is pipeline parallelism?
14. When would you horizontally scale inference?
15. How would you optimize GPU utilization?
16. How would you reduce inference cost?
17. What happens when inference traffic exceeds capacity?

## 11. Evaluation & Observability

1. Why is evaluating LLMs harder than evaluating traditional classifiers?
2. What is an evaluation dataset?
3. Offline versus online evaluation—when do you use each?
4. What is answer relevance?
5. What is faithfulness or groundedness?
6. How would you detect hallucinations?
7. What is LLM-as-a-Judge?
8. What are the risks of LLM-as-a-Judge?
9. When is human evaluation necessary?
10. What should you log from an AI request?
11. What is distributed tracing?
12. How would you trace a request through API → retrieval → model → tools?
13. Which production metrics would you monitor?
14. How would you build an AI feedback loop?
15. How would you detect a quality regression after changing a prompt?

## 12. AI Security & Safety

1. What is prompt injection?
2. What is indirect prompt injection?
3. How would you defend an RAG system against malicious retrieved content?
4. What is sensitive-data leakage?
5. How should secrets be handled in AI applications?
6. Why should model output never be blindly executed?
7. How would you validate structured model output?
8. How would you secure tool/function calling?
9. What is least privilege and how does it apply to agents?
10. How would you prevent excessive tool permissions?
11. How would you protect against denial-of-wallet attacks?
12. How would you audit AI actions?
13. What should happen when a safety check fails?
14. How would you design PII redaction?
15. How would you isolate tenants in a shared AI platform?

## 13. MLOps & Production AI

1. What is CI/CD for ML systems?
2. Why is model versioning different from normal code versioning?
3. How should datasets be versioned?
4. What is experiment tracking?
5. What is a model registry?
6. Explain a production ML pipeline from training to deployment.
7. How would you reproduce a historical model result?
8. What is model drift?
9. What is data drift?
10. How would you detect drift?
11. What is a canary deployment?
12. Compare canary and blue-green deployment.
13. How would you roll back a bad model release?
14. What should be monitored after deployment?
15. How would you containerize an AI service?
16. What belongs in a CI pipeline for an AI API?

## 14. AI System Design

1. Design a production AI chatbot.
2. Design a document Q&A system.
3. Design an enterprise RAG platform.
4. Design an AI agent that can execute business actions.
5. Design an LLM inference platform.
6. Design a multi-tenant AI API.
7. Design an AI recommendation system.
8. Design an AI summarization service processing millions of documents.
9. How would you estimate QPS, token throughput, storage, and GPU requirements?
10. Where would you use caching in an AI architecture?
11. Where would you use queues and asynchronous processing?
12. How would you handle dependency failures?
13. How would you design rate limiting?
14. How would you design observability?
15. How would you optimize cost while maintaining quality?
16. How would you choose between a managed API and self-hosted model?

## 15. Project & Behavioral Questions

1. Tell me about an AI project you built end-to-end.
2. What was the hardest technical problem you solved?
3. What production bug did you investigate and how did you find the root cause?
4. Tell me about a feature you designed and implemented.
5. What technical trade-off did you make and why?
6. Tell me about a time you disagreed with a technical decision.
7. How do you approach code reviews?
8. Tell me about a production incident you handled.
9. How do you prioritize competing engineering tasks?
10. Tell me about a time you were blocked and how you handled it.
11. How do you communicate technical risks to non-technical stakeholders?
12. Tell me about a time you improved system performance.
13. Tell me about a time you reduced infrastructure cost.
14. What would you improve in your previous AI system if you had another month?
15. Why do you want to work as an AI Engineer?

## Rapid-fire revision

- Python data structures, generators, decorators, async, testing, Big-O
- Probability, statistics, vectors, matrices, gradients, optimization
- Bias/variance, regularization, evaluation metrics, leakage
- Backpropagation, initialization, normalization, optimizers
- Attention, QKV, multi-head attention, positional encoding
- Tokenization, embeddings, context windows, decoding
- Prompting, structured outputs, tool calling, streaming
- RAG, chunking, embeddings, vector search, hybrid search, reranking
- Agents, ReAct, memory, state, orchestration, MCP
- Fine-tuning, PEFT, LoRA, QLoRA, quantization, DPO, RLHF
- GPU memory, batching, KV cache, inference serving, parallelism
- Evaluation, tracing, observability, regression testing
- Prompt injection, PII, tool security, least privilege
- Docker, CI/CD, model/data versioning, deployment, drift
- System design, capacity estimation, reliability, caching, queues, cost
- Your own projects, difficult bugs, trade-offs, deployment decisions, and STAR stories
