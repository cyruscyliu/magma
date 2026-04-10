<?php

enum E {
    case One;
    case Two;

    #[\Override]
    public function e(): void {}
}

echo "Done";

?>