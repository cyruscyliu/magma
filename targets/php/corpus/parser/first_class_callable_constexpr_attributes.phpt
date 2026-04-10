<?php

#[Attribute(Attribute::TARGET_CLASS | Attribute::IS_REPEATABLE)]
class Attr {
    public function __construct(public Closure $value) {
        var_dump($value('abc'));
    }
}

#[Attr(strrev(...))]
#[Attr(strlen(...))]
class C {}

foreach ((new ReflectionClass(C::class))->getAttributes() as $reflectionAttribute) {
    var_dump($reflectionAttribute->newInstance());
}

?>