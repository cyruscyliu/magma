<?php

class C {
    public private(set) static int $prop;
    public private(set) static array $prop2;
    public private(set) static stdClass $prop3;
    public private(set) static object $unset;

    public static function reset() {
        self::$prop = 1;
        self::$prop2 = [];
        self::$prop3 = new stdClass();
    }

    public static function setProp($prop) {
        self::$prop = $prop;
    }

    public static function addProp2($prop2) {
        self::$prop2[] = $prop2;
    }
}

function test() {
    C::reset();

    try {
        C::$prop = 2;
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump(C::$prop);

    C::setProp(3);
    var_dump(C::$prop);

    try {
        ++C::$prop;
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump(C::$prop);

    try {
        C::$prop++;
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump(C::$prop);

    try {
        C::$prop += str_repeat('a', 10);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump(C::$prop);

    try {
        $ref = &C::$prop;
        $ref++;
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump(C::$prop);

    try {
        $ref = 4;
        C::$prop = &$ref;
        $ref++;
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump(C::$prop);

    try {
        C::$prop2[] = 'foo';
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump(C::$prop2);

    C::addProp2('bar');
    var_dump(C::$prop2);

    C::$prop3->foo = 'foo';
    var_dump(C::$prop3);

    unset(C::$unset->foo);
}

test();
echo "\nRepeat:\n";
test();

?>