<?php

class C {
    public function __construct(
        #[\Override]
        public mixed $c,
    ) {}
}

echo "Done";

?>