<?php

class A {
    public string|int $prop { get => $this->prop; }
}

class B extends A {
    public string $prop { get => 'foo'; }
}

?>