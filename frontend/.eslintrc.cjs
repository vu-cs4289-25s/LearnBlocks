module.exports = {
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.json', './tsconfig.node.json'],
    tsconfigRootDir: __dirname,
  },
  plugins: [
    '@typescript-eslint',
    'react',
    'prettier', // This enables prettier as an ESLint plugin
  ],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/strict-type-checked', // Even stricter type rules (uncomment if preferred)
    'plugin:react/recommended',
    'plugin:react/jsx-runtime',
    'plugin:prettier/recommended', // This should be last to override conflicting rules
  ],
  rules: {
    // You can further configure or override rules here.
    // For instance, you might enforce prettier errors:
    // "prettier/prettier": "error",
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
