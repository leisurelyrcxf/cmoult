package model.listeners;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import model.Listener;

/* Opens a socket server for users to supply updates. */
public class SocketListener extends Listener implements Runnable {

	private static int Listener_port = 4242;
	private static String Invoke_message = "update";

	private final int port = Listener_port;
	private boolean keep_running = true;
	private int update_thread_index = 0;
	private Thread thread;

	/* Constructor using the same parameters as a regular thread object */
	public SocketListener() {
		this.thread = new Thread(this, "Pymoult Listener");
		this.thread.setDaemon(true);
	}

	/* Load the update code and runs it in a new thread */
	private void start_update(String update_address) {
		Path path = Paths.get(update_address);
		if (Files.exists(path)) {
			Runnable update = () -> {
				System.out.println("on charge le nouveau module!");
				// Choisisse le manager et y enregistre l'update
			};
			Thread update_thread = new Thread(update, "update thread "
					+ this.update_thread_index);
			update_thread.start();
			this.update_thread_index += 1;
		} else
			System.out.println("Error : the update module supplied was not found");
	}

	/* Main loop of the thread, opens the socket and parses the commands */
	public void run() {
		try (ServerSocket serverSocket = new ServerSocket(this.port)) {
			while (this.keep_running) {
				try (Socket socket = serverSocket.accept();
				     BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
					String str = br.readLine();
					if (str.startsWith(Invoke_message)) {
						String update_address = str.substring(Invoke_message.length());
						this.start_update(update_address);
					}
				}
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	@Override
	public void start() {
		this.thread.start();
	}

	@Override
	public void stop() {
		// Thread is a daemon
	}

}
