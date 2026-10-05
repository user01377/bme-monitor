## Development Setup

To develop this React project, you will need **Node.js and npm** installed on your machine.

### 1. Install Node.js and npm

Download and install Node.js from the official website:

https://nodejs.org/en/download

Installing Node.js also installs **npm (Node Package Manager)**, which this project uses to manage its dependencies.

npm is responsible for:

* Installing project dependencies
* Managing package versions
* Generating and maintaining the `package-lock.json` file

### 2. Install Dependencies

From the project root, navigate into the `dashboard/` directory:

```bash
cd dashboard/
```

Then install the project's dependencies:

```bash
npm install
```

This will read the project's `package.json` file and install all required dependencies into `node_modules/`.

### 3. Start the Development Server

From the `dashboard/` directory, run:

```bash
npm run dev
```

This will start the **Vite development server**, which will be available at:

```text
http://localhost:5173
```

While the development server is running, changes to the React application will automatically appear in the browser through **Hot Module Replacement (HMR)**. You generally do not need to manually refresh the page while developing.

**Development workflow:**

1. Start the Vite server with `npm run dev`
2. Open `http://localhost:5173` in your browser
3. Make changes to the React code
4. Vite will automatically update the page with your changes
