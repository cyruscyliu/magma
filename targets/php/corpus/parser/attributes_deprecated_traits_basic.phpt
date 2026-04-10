<?php

#[\Deprecated("please do not use")]
trait DemoTrait1 {}

#[\Deprecated("will be removed in 3.0", since: "2.7")]
trait DemoTrait2 {}

#[\Deprecated(message: "going away")]
trait DemoTrait3 {}

#[\Deprecated(since: "3.5")]
trait DemoTrait4 {}

class DemoClass {
	use DemoTrait1;
	use DemoTrait2;
	use DemoTrait3;
	use DemoTrait4;
}

?>