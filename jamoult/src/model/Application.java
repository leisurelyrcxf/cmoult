package model;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class Application {
	private Map<String,Manager> managers = new HashMap<String, Manager>();
	private List<Listener> listeners = new LinkedList<Listener>();
	private List<String> history = new LinkedList<String>();
	
	public void register(String name, Manager manager) {
		this.managers.put(name, manager);
	}

	public void unRegister(String name) {
		this.managers.remove(name);
	}
	
	public Manager getManager(String name) {
		return this.managers.get(name);
	}
	
	public void main(String[] args) {
		/* création des listeners et managers statiques */
		/* démarrage des listeners statiques */
		for (Listener l : this.listeners)
			l.start();
		/* code principal de l'application */
		/* arrêt des listeners et managers statiques */
		for (Listener l : this.listeners)
			l.stop();
		for (Manager m : this.managers.values())
			m.stop();
	}

	public void addCompletedUpdate(String name) {
		this.history.add(name);		
	}
}
