# AI-multimodal-weaviate
Multi-Modal Search with Weaviate Vector Databases created during DeepLearningAI workshop.


## Initial Setup

Install Weaviate Python Client

Run the following command:
```
pip install --pre -I "weaviate-client==4.*"
```

## Deploy Weaviate vector DB

We can use with 3 different options:

- **Embedded** is integrated within the application directly.
- **Self-Hosted (Docker)** involves containerization for deployment on self-managed infrastructure.
- **Cloud Deployment** utilizes cloud services for hosting, offering scalability and managed services, but with dependency and cost considerations.

### Embedded Deployment

Embedded deployment involves incorporating a software component directly into an application or system. In the case of Weaviate, this means integrating Weaviate's functionality as a library or module within the application's codebase.

#### Pros

- **Simplified Integration:** Easy incorporation into the application's logic.
- **Performance:** Often leads to faster responses due to reduced latency (no external API calls).
- **Customization:** Allows for specific customization to suit the application's needs.

#### Cons

- **Resource Utilization:** Might increase resource utilization within the application.
- **Maintenance:** Can complicate updates and maintenance as it's tied directly to the application's code.

### Self-Hosted (Docker) Deployment

Self-hosted deployment typically involves using containerization technologies like Docker to run services such as Weaviate within containers. Users deploy and manage these containers on their own infrastructure or servers.

#### Pros:

- **Portability:** Docker containers are highly portable across different environments.
- **Isolation:** Provides a level of isolation and reproducibility for the service.
- **Ease of Management:** Simplified deployment and scaling using container orchestration tools.

#### Cons

- **Infrastructure Management:** Requires managing and maintaining the infrastructure or servers hosting the containers.
- **Learning Curve:** Might involve a learning curve for Docker and container orchestration tools.

### Cloud Deployment

Cloud deployment involves using cloud service providers (like Azure, AWS, or GCP) to provision and manage the service, such as Weaviate, without worrying about underlying infrastructure.

#### Pros

- **Scalability:** Easily scalable by leveraging cloud resources.
- **Managed Services:** Often includes managed services, reducing the burden of maintenance.
- **Global Availability:** Can be accessed globally with high availability.

#### Cons

- **Costs:** Can incur costs based on usage or subscription models.
- **Dependency on Provider:** Relies on the cloud service provider's infrastructure and may have constraints based on their offerings.

PS: in this repository you can found a docker compose file. You can navigate to this directory and run `docker-compose up -d` to run it and `docker ps` to confirm if is it running (http://localhost:8080). 




