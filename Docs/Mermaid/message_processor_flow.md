graph TD
    A[Start Message Processor] --> B[Initialize MongoDB]
    B --> C[Create Kafka Consumer]
    C --> D[Start Consumer]
    D --> E[Wait for Message]
    E --> F{Message Received?}
    F -->|Yes| G[Process Message]
    G --> H[Insert into MongoDB]
    H --> E
    F -->|No| I{Stop Requested?}
    I -->|No| E
    I -->|Yes| J[Stop Consumer]
    J --> K[End]
