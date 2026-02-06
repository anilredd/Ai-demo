package main.java;

public class App {
    public static void main(String[] args) {
        // 1. Secure password handling via environment variable
        String password = System.getenv("APP_PASSWORD");
        if (password == null || password.isEmpty()) {
            System.out.println("❌ APP_PASSWORD is not set. Exiting safely.");
            System.exit(1);
        }

        // Avoid printing the actual password
        System.out.println("Password loaded securely.");

        // 2. Null-safe string handling
        String text = null; // could come from user input, database, etc.
        if (text != null) {
            System.out.println("Text length: " + text.length());
        } else {
            System.out.println("Text is null, skipping length check.");
        }

        // 3. Normal execution
        System.out.println("✅ Application executed safely.");
    }
}