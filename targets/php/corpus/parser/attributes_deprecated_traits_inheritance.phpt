<?php

#[\Deprecated]
trait DemoTrait {}

class DemoClass {
	use DemoTrait;
}

class ChildClass extends DemoClass {
}

?>