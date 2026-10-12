<?php

#[\Deprecated]
trait DemoTraitA {}

trait DemoTraitB {
	use DemoTraitA;
}

class DemoClass {
	use DemoTraitB;
}

?>