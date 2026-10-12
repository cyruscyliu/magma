<?php

namespace Test;

class Clazz {
	#[Attr(strrev(...), \strrev(...), Clazz::foo(...), self::foo(...))]
	function foo() { }
}

$r = new \ReflectionMethod(Clazz::class, 'foo');
foreach ($r->getAttributes() as $attribute) {
    echo $attribute;
}

?>