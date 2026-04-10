<?php

enum E {
	#[\Deprecated]
	case Test;

	#[\Deprecated("use E::Test instead")]
	case Test2;
}

E::Test;
E::Test2;

?>