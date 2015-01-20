package lowlevel.data_access;

import java.lang.ref.WeakReference;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Queue;

/* Iterator that will give access to all instances of a given class,
    using either immediate or progressive strategy */
public class DataAccessor<T> implements Iterable<T> {
	private final Queue<T> queue = new LinkedList<T>();
	private Class<T> tclass;
	private Strategy strategy = Strategy.Immediate;
		
	/* Constructor. Takes the class whose instances are to be accessed and
    the strategy to be used as arguments */
    public DataAccessor(Class<T> tclass, Strategy strategy) {
        this.tclass = tclass;	
        this.strategy = strategy;
    }
    
    /* When using the immediate strategy, gets all instances of the
        given class from the pool.

        When using the progressive strategy, used the metaobject
        protocol, binding routers to the __getattribute__ and
        __setattr__ methods of the given class.*/	
	@Override
	public Iterator<T> iterator() {
		// TODO 
		if (this.strategy == Strategy.Immediate) {
			ObjectsPool pool = ObjectsPool.getObjectsPool();
            pool.begin_use();
            for (WeakReference<Object> ref : pool) {
            	Object obj = ref.get();
            	if (tclass.isInstance(obj))
            		this.queue.add(tclass.cast(obj));
            }
            pool.end_use();
		}
		return this.queue.iterator();
	}

}
