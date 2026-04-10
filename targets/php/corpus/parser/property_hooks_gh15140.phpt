<?php

interface I {
    public string $prop {
        set(int|string $value);
    }
}
class C implements I {
    public string $prop;
}

?>