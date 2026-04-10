<?php

spl_autoload_register(static function ($className) {
    if ($className === 'C') {
        require(__DIR__ . '/attributes_autoload.inc');
    }
});

#[Attribute(Attribute::TARGET_CLASS | Attribute::IS_REPEATABLE)]
class Attr {
    public function __construct(public Closure $value) {
        $value('foo');
    }
}

foreach ((new ReflectionClass(C::class))->getAttributes() as $reflectionAttribute) {
    var_dump($reflectionAttribute->newInstance());
}

?>