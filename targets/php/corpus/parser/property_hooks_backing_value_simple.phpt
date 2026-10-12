<?php

class C {
    public $switch;

    public $prop = 42 {
        get {
            echo __METHOD__, "\n";
            if ($this->switch) {
                $other = new C();
                $other->switch = false;
            } else {
                $other = $this;
            }
            var_dump($other->prop);
            return 1;
        }
        set => $this->prop;
    }
}

function test() {
    $c = new C();
    $c->switch = true;
    var_dump($c->prop);
}

test();
test();

?>