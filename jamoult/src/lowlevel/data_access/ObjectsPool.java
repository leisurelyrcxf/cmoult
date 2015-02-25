package lowlevel.data_access;

import java.lang.ref.WeakReference;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

public class ObjectsPool implements Iterable<WeakReference<Object>> {
    private static ObjectsPool objectsPool;
    
    /* Returns the instance of ObjectsPool. Raises an error if no
        ObjectsPoolinstance was created */
    public static ObjectsPool getObjectsPool() {
        if (ObjectsPool.objectsPool == null)
        	ObjectsPool.objectsPool = new ObjectsPool();
        return ObjectsPool.objectsPool;
    }
    
	private boolean in_use = false;
    private Set<WeakReference<Object>> objects = new HashSet<WeakReference<Object>>();
	private Set<WeakReference<Object>> buffer = new HashSet<WeakReference<Object>>();

    private ObjectsPool() {
        /* set_instance_hook(ObjectsPool.objectsPool.add) */
    }
    
    /* Adds a weak reference to the object given as argument */
    public void add(Object obj) {
        if (this.in_use )
            this.buffer.add(new WeakReference<Object>(obj));
        else
            this.objects.add(new WeakReference<Object>(obj));
    }

	public void begin_use() {
		this.in_use = true;
	}

	public void end_use() {
		this.in_use = false;
		this.merge();
	}

	private synchronized void merge() {
        this.objects.addAll(this.buffer);
        this.buffer.clear();
	}

	@Override
	public Iterator<WeakReference<Object>> iterator() {
		return this.objects.iterator();
	}

}
