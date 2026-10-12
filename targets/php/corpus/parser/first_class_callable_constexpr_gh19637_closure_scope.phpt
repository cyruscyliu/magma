<?php

#[Attribute(Attribute::TARGET_CLASS)]
class Attr {
    public function __construct(public array $value) {}
}

class F {
    public static function foreign() {}
}

class G extends F { }

#[Attr([
    F::foreign(...),
    G::foreign(...),
    self::myMethod(...),
    strrev(...),
])]
class C {
    private static function myMethod(string $foo) {
        return "XXX";
    }

    public static function foo() {
        foreach ([
            F::foreign(...),
            G::foreign(...),
            self::myMethod(...),
            strrev(...),
        ] as $fn) {
            $r = new \ReflectionFunction($fn);
            var_dump($r->getClosureCalledClass());
            var_dump($r->getClosureScopeClass());
        }
    }
}
 
foreach ((new ReflectionClass(C::class))->getAttributes() as $reflectionAttribute) {
    foreach ($reflectionAttribute->newInstance()->value as $fn) {
        $r = new \ReflectionFunction($fn);
        var_dump($r->getClosureCalledClass());
        var_dump($r->getClosureScopeClass());
    }
}
echo "=======\n";
C::foo();

?>