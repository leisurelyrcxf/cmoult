package lowlevel.data_update;

import lowlevel.data_access.Transformer;
import model.ReconfUnit;

public class API {
	/* Updates a given object to a given class. If a trasformer is given
	    in argument, applies it to the object */
	public static void updateToClass(ReconfUnit obj,Class<?> nclass,Transformer transformer) {
	    /* obj.__class__ = nclass */
	    if (transformer != null) {
	    	transformer.transform(obj);
	    	nclass.cast(obj);
	    }
	}
}
