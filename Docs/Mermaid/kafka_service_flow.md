graph TD
    A[KafkaService Class] --> B[Initialize]
    B --> C[Start Method]
    C --> D[Create AIOKafkaProducer]
    D --> E[Start Producer]
    E --> F[Send Message Method]
    F --> G{Message Sent?}
    G -->|Yes| H[Return]
    G -->|No| I[Retry/Error Handling]
    I --> F
    B --> J[Stop Method]
    J --> K[Stop Producer]
    K --> L[End]