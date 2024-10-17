graph TD
    A[Start] --> B[Download Media Function]
    B --> C{Has Media?}
    C -->|Yes| D[Download File]
    D --> E[Process Media File]
    E --> F[Return Media Info]
    C -->|No| G[Return None]
    A --> H[Download Media Batch Function]
    H --> I[Iterate Messages]
    I --> J[Download Media for Each]
    J --> K[Return Media Info List]