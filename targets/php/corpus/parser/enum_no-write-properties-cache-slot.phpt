<?php

enum Test {
    case A;

    public function modify() {
        // Cache slots for the read and write are merged.
        var_dump($this->name);
        $this->name = 'foobar';
    }
}

try {
    Test::A->modify();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump(Test::A->name);

?>