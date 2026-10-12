<?php

interface X {}
interface Y extends X {}

class Test {
    public Y $prop {
        set(X $prop) {}
    }
}

?>
===DONE===