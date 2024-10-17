graph TD
    A[Start] --> B[Calculate File Hash]
    B --> C[Find Existing File]
    C --> D{File Exists?}
    D -->|Yes| E[Return Existing Path]
    D -->|No| F[Save File Hash]
    F --> G[Return New Path]
    A --> H[Process Media File]
    H --> I{File Size OK?}
    I -->|Yes| J[Calculate Hash]
    J --> K[Find or Save File]
    I -->|No| L[Remove File]
    L --> M[Return None]
    K --> N[Return File Path]