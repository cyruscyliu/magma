<?php

#[\AllowDynamicProperties]
class A {
    private $priv = 'priv A';
    private $privA = 'privA';
    protected $prot = 'prot';
    public $pubA = 'pubA';

    public static $static = 'static';

    public $noDefault;
    public string $noDefaultTyped;
    public $initialized;

    public $hooked {
        get { return $this->hooked; }
        set ($value) { $this->hooked = strtoupper($value); }
    }

    public $virtual {
        get { return 'virtual'; }
        set ($value) { }
    }
}

class B extends A {
    private $priv = 'privB';
    public $pubB = 'pubB';

    private readonly string $readonly;
}

set_error_handler(function ($errno, $errstr) {
    throw new Error($errstr);
});

function testProperty(callable $makeObj, $propReflector) {

    $reflector = new ReflectionClass(B::class);

    $getValue = function ($obj, $propReflector) {
        $name = $propReflector->getName();
        return $obj->$name;
    };

    printf("\n## %s", $propReflector);

    printf("\nskipInitializerForProperty():\n");
    $obj = $makeObj();
    $skept = false;
    try {
        $propReflector->skipLazyInitialization($obj);
        $skept = true;
    } catch (ReflectionException $e) {
        printf("%s: %s\n", $e::class, $e->getMessage());
    }
    if (!$reflector->isUninitializedLazyObject($obj)) {
        printf("Object was unexpectedly initialized (1)\n");
    }
    if ($skept) {
        try {
            printf("getValue(): ");
            var_dump($getValue($obj, $propReflector));
        } catch (\Error $e) {
            printf("%s: %s\n", $e::class, $e->getMessage());
        }
        if (!$propReflector->isStatic()) {
            $propReflector->setValue($obj, '');
        }
        if (!$reflector->isUninitializedLazyObject($obj)) {
            printf("Object was unexpectedly initialized (1)\n");
        }
    }

    printf("\nsetRawValueWithoutLazyInitialization():\n");
    $obj = $makeObj();
    $skept = false;
    try {
        $propReflector->setRawValueWithoutLazyInitialization($obj, 'value');
        $skept = true;
    } catch (ReflectionException $e) {
        printf("%s: %s\n", $e::class, $e->getMessage());
    }
    if (!$reflector->isUninitializedLazyObject($obj)) {
        printf("Object was unexpectedly initialized (1)\n");
    }
    if ($skept) {
        try {
            printf("getValue(): ");
            var_dump($getValue($obj, $propReflector));
        } catch (\Error $e) {
            printf("%s: %s\n", $e::class, $e->getMessage());
        }
        if (!$reflector->isUninitializedLazyObject($obj)) {
            printf("Object was unexpectedly initialized (1)\n");
        }
    }
}

function test(string $name, callable $makeObj) {
    printf("# %s:\n", $name);

    $reflector = new ReflectionClass(B::class);

    foreach ($reflector->getProperties() as $propReflector) {
        testProperty($makeObj, $propReflector);
    }

    testProperty($makeObj, new class {
        function getName() {
            return 'dynamicProp';
        }
        function setValue($obj, $value) {
            $obj->dynamicProp = $value;
        }
        function isStatic() {
            return false;
        }
        // TODO: refactor this test
        function skipLazyInitialization(object $object) {
            throw new \ReflectionException();
        }
        function setRawValueWithoutLazyInitialization(object $object) {
            throw new \ReflectionException();
        }
        function __toString() {
            return "Property [ \$dynamicProp ]\n";
        }
    });
}

$reflector = new ReflectionClass(B::class);

$factory = function () use ($reflector) {
    return $reflector->newLazyGhost(function ($obj) {
        throw new \Exception('initializer');
    });
};

test('Ghost', $factory);

$factory = function () use ($reflector) {
    return $reflector->newLazyGhost(function ($obj) {
        throw new \Exception('initializer');
    });
};

test('Proxy', $factory);

?>