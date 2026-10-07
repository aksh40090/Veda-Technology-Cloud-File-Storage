# Viva Quick Answers
1. **Why Flask?** Lightweight Python framework suitable for a small web/API project.
2. **What is object storage?** Data stored as objects with a unique key and metadata, such as S3.
3. **Why separate metadata?** It makes searching and filtering easier and keeps binary objects separate.
4. **Why validate files?** To restrict unsupported files and reduce security risk.
5. **Why environment variables?** Secrets must not be exposed in frontend code or GitHub.
6. **What is S3?** Amazon's object storage service.
7. **How does download work?** Flask retrieves the object and sends it to the browser as an attachment.
8. **How can it become production-ready?** Add authentication, authorization, signed URLs, encryption, scanning, rate limiting and auditing.
