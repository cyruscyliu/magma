<?php

trait T {
    public mixed $t;
}

class C {
    use T;

    #[\Override]
    public mixed $t;
}

echo "Done";

?>