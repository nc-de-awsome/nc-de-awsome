### Hi there 👋

<!--
**nc-de-awsome/nc-de-awsome** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->

1. Fork and clone this project.
2. In the terminal, navigate to the root directory of the project, and run:

   ```bash
   sh setup.sh
   ```

   This creates venv and installs project requirements.

3. Following this, in the terminal, navigate to the root directory of the project, and run:

   ```bash
   sh state.sh
   ```

   THis creates an s3 bucket that will store the terraform state file remotely.

4. Deployment of AWS resources are automated using GitHub Actions.
