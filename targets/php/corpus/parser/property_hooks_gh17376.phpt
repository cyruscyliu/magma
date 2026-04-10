<?php

class A {
    public $prop = 1;
}

class B extends A {
    public $prop = 1 {
        get {
            echo __METHOD__, "\n";
            return $this->prop;
        }
        set {
            echo __METHOD__, "\n";
            $this->prop = $value;
        }
    }
}

function test(A $a) {
    echo "read\n";
    var_dump($a->prop);
    echo "write\n";
    $a->prop = 42;
    echo "read-write\n";
    $a->prop += 43;
    echo "pre-inc\n";
    ++$a->prop;
    echo "pre-dec\n";
    --$a->prop;
    echo "post-inc\n";
    $a->prop++;
    echo "post-dec\n";
    $a->prop--;
}

echo "A\n";
test(new A);

echo "\nA\n";
test(new A);

echo "\nB\n";
test(new B);

echo "\nB\n";
test(new B);

?>