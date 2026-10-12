<?php

#[\Deprecated]
trait DemoTraitA {}

#[\Deprecated]
trait DemoTraitB {}

trait DemoTraitC {}

class DemoClass {
	use DemoTraitA, DemoTraitB, DemoTraitC;
}

?>