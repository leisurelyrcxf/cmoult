package lowlevel.data_update;

import model.ReconfUnit;
import model.UpdateFunction;

public class API {
	/* Updates a given object to a given class. If a trasformer is given
	    in argument, applies it to the object */
	public static void updateToClass(ReconfUnit obj,Class<?> nclass,UpdateFunction transformer) {
	    /* obj.__class__ = nclass */
	    if (transformer != null) {
	    	obj.update(transformer);
	    	nclass.cast(obj);
	    }
	}
}
