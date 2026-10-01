"""Built-in market dataset: skill catalog + role requirements (importance 3=critical, 2=important, 1=nice to have)."""

# name: (category, aliases to detect in text, weeks to learn, suggested resource)
CATALOG = {
    "Python": ("Languages", ["python", "python3"], 6, "Python for Everybody (Coursera)"),
    "Java": ("Languages", ["java"], 8, "MOOC.fi Java Programming"),
    "JavaScript": ("Languages", ["javascript", "js", "es6"], 6, "javascript.info"),
    "TypeScript": ("Languages", ["typescript", "ts"], 3, "TypeScript Handbook"),
    "R": ("Languages", ["r programming", "rstudio", "r language"], 5, "R for Data Science (book)"),
    "HTML/CSS": ("Web & APIs", ["html", "html5", "css", "css3", "sass", "tailwind"], 3, "MDN Learn Web Development"),
    "React": ("Web & APIs", ["react", "react.js", "reactjs", "next.js"], 5, "react.dev tutorial"),
    "Node.js": ("Web & APIs", ["node.js", "nodejs", "node", "express"], 4, "The Odin Project: NodeJS"),
    "REST APIs": ("Web & APIs", ["rest", "rest api", "restful", "api development", "graphql"], 3, "RESTful API design guide (Microsoft)"),
    "Django": ("Web & APIs", ["django"], 4, "Django official tutorial"),
    "FastAPI": ("Web & APIs", ["fastapi", "flask"], 2, "FastAPI official tutorial"),
    "SQL": ("Databases", ["sql", "mysql", "postgresql", "postgres", "sqlite", "t-sql"], 4, "Mode SQL Tutorial"),
    "MongoDB": ("Databases", ["mongodb", "nosql", "redis", "dynamodb"], 3, "MongoDB University M001"),
    "Excel": ("Data & Analytics", ["excel", "spreadsheets", "google sheets", "pivot tables"], 3, "Excel Skills for Business (Coursera)"),
    "Statistics": ("Data & Analytics", ["statistics", "statistical", "hypothesis testing", "probability", "a/b testing"], 6, "Khan Academy Statistics"),
    "Pandas": ("Data & Analytics", ["pandas"], 3, "Kaggle Pandas micro-course"),
    "NumPy": ("Data & Analytics", ["numpy", "scipy"], 2, "NumPy quickstart"),
    "Data Visualization": ("Data & Analytics", ["tableau", "power bi", "powerbi", "matplotlib", "seaborn", "plotly", "data visualization", "looker"], 4, "Tableau / Power BI free learning paths"),
    "ETL": ("Data & Analytics", ["etl", "elt", "data pipelines", "data pipeline", "dbt"], 5, "Data Engineering Zoomcamp"),
    "Apache Spark": ("Data & Analytics", ["spark", "pyspark", "hadoop", "databricks", "kafka"], 6, "Databricks Academy (free)"),
    "Airflow": ("Data & Analytics", ["airflow", "prefect", "dagster"], 3, "Apache Airflow official tutorial"),
    "Data Warehousing": ("Data & Analytics", ["data warehouse", "data warehousing", "snowflake", "bigquery", "redshift"], 4, "Snowflake / BigQuery quickstarts"),
    "Machine Learning": ("Machine Learning", ["machine learning", "ml", "scikit-learn", "sklearn", "xgboost"], 10, "Andrew Ng ML Specialization"),
    "Deep Learning": ("Machine Learning", ["deep learning", "neural networks", "cnn", "rnn", "tensorflow", "keras"], 8, "fast.ai Practical Deep Learning"),
    "PyTorch": ("Machine Learning", ["pytorch", "torch"], 4, "PyTorch official tutorials"),
    "NLP & LLMs": ("Machine Learning", ["nlp", "natural language processing", "llm", "llms", "transformers", "langchain", "generative ai", "genai", "hugging face"], 6, "Hugging Face NLP Course"),
    "MLOps": ("Machine Learning", ["mlops", "mlflow", "model deployment", "kubeflow", "model serving"], 5, "MLOps Zoomcamp"),
    "Git": ("Engineering Practices", ["git", "github", "gitlab", "version control"], 1, "Pro Git (book)"),
    "Testing": ("Engineering Practices", ["unit testing", "pytest", "jest", "testing", "tdd", "selenium"], 2, "Test-Driven Development by Example"),
    "CI/CD": ("Engineering Practices", ["ci/cd", "cicd", "jenkins", "github actions", "gitlab ci", "continuous integration"], 3, "GitHub Actions documentation"),
    "System Design": ("Engineering Practices", ["system design", "microservices", "distributed systems", "scalability"], 8, "Designing Data-Intensive Applications"),
    "Data Structures & Algorithms": ("Engineering Practices", ["data structures", "algorithms", "dsa", "leetcode"], 10, "NeetCode roadmap"),
    "Docker": ("Cloud & DevOps", ["docker", "containers", "containerization"], 2, "Docker Get Started guide"),
    "Kubernetes": ("Cloud & DevOps", ["kubernetes", "k8s", "helm"], 6, "Kubernetes Basics (kubernetes.io)"),
    "Terraform": ("Cloud & DevOps", ["terraform", "infrastructure as code", "iac", "ansible", "cloudformation"], 4, "HashiCorp Terraform tutorials"),
    "AWS": ("Cloud & DevOps", ["aws", "amazon web services", "ec2", "s3", "lambda"], 8, "AWS Cloud Practitioner Essentials"),
    "Azure": ("Cloud & DevOps", ["azure", "microsoft azure"], 6, "Microsoft Learn AZ-900"),
    "GCP": ("Cloud & DevOps", ["gcp", "google cloud"], 6, "Google Cloud Skills Boost"),
    "Linux": ("Cloud & DevOps", ["linux", "bash", "shell scripting", "unix"], 4, "Linux Journey"),
    "Monitoring": ("Cloud & DevOps", ["monitoring", "prometheus", "grafana", "datadog", "observability"], 3, "Prometheus + Grafana getting started"),
    "Networking": ("Cloud & DevOps", ["networking", "tcp/ip", "dns", "firewalls", "vpn", "load balancing"], 5, "Computer Networking (Cisco NetAcad)"),
    "Cybersecurity Fundamentals": ("Security", ["cybersecurity", "information security", "infosec", "owasp", "security+", "vulnerability"], 6, "CompTIA Security+ / TryHackMe"),
    "SIEM & Threat Detection": ("Security", ["siem", "splunk", "threat detection", "incident response", "soc"], 5, "Splunk Fundamentals (free)"),
    "Penetration Testing": ("Security", ["penetration testing", "pentest", "pentesting", "kali", "metasploit", "burp suite"], 8, "TryHackMe Jr Penetration Tester"),
    "Cryptography": ("Security", ["cryptography", "encryption", "pki", "tls"], 4, "Cryptography I (Coursera)"),
    "Communication": ("Soft Skills", ["communication", "presentation", "stakeholder", "storytelling", "collaboration"], 4, "Practice: write up & present your projects"),
    "Problem Solving": ("Soft Skills", ["problem solving", "problem-solving", "analytical", "critical thinking"], 3, "Showcase case studies in your portfolio"),
    "Agile & Scrum": ("Soft Skills", ["agile", "scrum", "kanban", "jira"], 1, "Scrum Guide (free)"),
}

ROLES = {
    "Data Scientist": {
        "desc": "Turns messy data into models and decisions.",
        "skills": {"Python": 3, "SQL": 3, "Statistics": 3, "Pandas": 3, "Machine Learning": 3, "NumPy": 2,
                   "Data Visualization": 2, "Deep Learning": 2, "Git": 2, "Communication": 2, "Problem Solving": 2,
                   "NLP & LLMs": 1, "Apache Spark": 1, "AWS": 1, "Excel": 1}},
    "Data Analyst": {
        "desc": "Finds answers in business data and explains them clearly.",
        "skills": {"SQL": 3, "Excel": 3, "Data Visualization": 3, "Communication": 3, "Statistics": 2, "Python": 2,
                   "Pandas": 2, "Problem Solving": 2, "ETL": 1, "R": 1}},
    "Machine Learning Engineer": {
        "desc": "Ships and maintains ML models in production.",
        "skills": {"Python": 3, "Machine Learning": 3, "MLOps": 3, "Deep Learning": 2, "PyTorch": 2, "Docker": 2,
                   "Git": 2, "Data Structures & Algorithms": 2, "NLP & LLMs": 2, "AWS": 1, "Kubernetes": 1, "CI/CD": 1}},
    "Backend Developer": {
        "desc": "Builds the APIs, services and databases behind apps.",
        "skills": {"REST APIs": 3, "SQL": 3, "Git": 3, "Python": 2, "System Design": 2, "Docker": 2, "Testing": 2,
                   "CI/CD": 2, "Data Structures & Algorithms": 2, "Java": 1, "Node.js": 1, "MongoDB": 1, "Django": 1,
                   "FastAPI": 1, "Linux": 1, "AWS": 1}},
    "Frontend Developer": {
        "desc": "Builds fast, accessible interfaces people enjoy using.",
        "skills": {"JavaScript": 3, "HTML/CSS": 3, "React": 3, "Git": 3, "TypeScript": 2, "REST APIs": 2, "Testing": 2,
                   "Problem Solving": 2, "Node.js": 1, "Agile & Scrum": 1}},
    "Full Stack Developer": {
        "desc": "Owns features from the database to the browser.",
        "skills": {"JavaScript": 3, "REST APIs": 3, "Git": 3, "React": 2, "Node.js": 2, "HTML/CSS": 2, "SQL": 2,
                   "TypeScript": 1, "MongoDB": 1, "Docker": 1, "Testing": 1, "System Design": 1, "CI/CD": 1, "AWS": 1}},
    "DevOps Engineer": {
        "desc": "Automates building, deploying and running software.",
        "skills": {"Linux": 3, "Docker": 3, "Kubernetes": 3, "CI/CD": 3, "Git": 3, "Terraform": 2, "AWS": 2,
                   "Python": 2, "Monitoring": 2, "Networking": 1, "Azure": 1}},
    "Cloud Engineer": {
        "desc": "Designs and operates secure, scalable cloud infrastructure.",
        "skills": {"AWS": 3, "Linux": 2, "Terraform": 2, "Networking": 2, "Docker": 2, "CI/CD": 2, "Azure": 1,
                   "GCP": 1, "Kubernetes": 1, "Python": 1, "Cybersecurity Fundamentals": 1, "Monitoring": 1}},
    "Data Engineer": {
        "desc": "Builds the pipelines and warehouses analysts rely on.",
        "skills": {"Python": 3, "SQL": 3, "ETL": 3, "Data Warehousing": 3, "Apache Spark": 2, "Airflow": 2, "AWS": 2,
                   "Git": 2, "Docker": 1, "Linux": 1, "MongoDB": 1}},
    "Cybersecurity Analyst": {
        "desc": "Detects, investigates and prevents security threats.",
        "skills": {"Cybersecurity Fundamentals": 3, "Networking": 3, "SIEM & Threat Detection": 3, "Linux": 2,
                   "Penetration Testing": 2, "Cryptography": 2, "Communication": 2, "Problem Solving": 2,
                   "Python": 1, "AWS": 1}},
}

PRIORITY = {3: "Critical", 2: "Important", 1: "Nice to have"}
