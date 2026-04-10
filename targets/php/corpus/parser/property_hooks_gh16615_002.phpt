<?php

class Foo {
    public string $bar {
        set => $value;
    }
    public function __clone() {
        try {
            echo $this->bar;
        } catch (Error $e) {
            printf("%s: %s\n", $e::class, $e->getMessage());
        }
    }
}

// Adds IS_PROP_REINITABLE to prop flags
clone new Foo();

?>