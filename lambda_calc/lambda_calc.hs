data Link = Zero | Succ Link deriving (Eq, Ord, Show)

data Term = Var Link | Abs Term | App Term Term deriving (Eq, Show)

lift :: Link -> Term -> Term
lift n (Var a) | a >= n = Var (Succ a)
lift n (Var a) = Var a
lift n (Abs t) = Abs (lift (Succ n) t)
lift n (App p q) = App (lift n p) (lift n q)

sbst :: Link -> Term -> Term -> Term
sbst n x (Var (Succ a)) | a >= n = Var a
sbst n x (Var a) | a == n = x
sbst n x (Var a) = Var a
sbst n x (Abs t) = Abs (sbst (Succ n) (lift Zero x) t)
sbst n x (App p q) = App (sbst n x p) (sbst n x q)

step :: Term -> Term
step (App (Abs t) s) = sbst Zero (step s) (step t)
step (Var a) = Var a
step (Abs t) = Abs (step t)
step (App p q) = App (step p) (step q)

beta :: Term -> Term
beta x = if x == step x then x else beta (step x)

enum :: Link -> [Link]
enum Zero = []
enum (Succ n) = Zero : map Succ (enum n)

wire :: Link -> Term -> [Term]
wire n (Var _) = map Var (enum n)
wire n (Abs t) = map Abs (wire (Succ n) t)
wire n (App p q) = [App i j | i <- wire n p, j <- wire n q]

trees :: Link -> [Term]
trees Zero = [Var Zero]
trees (Succ n) =
  map Abs (trees n)
    ++ [App x y | i <- enum n, x <- trees i, y <- trees n]
    ++ [App x y | i <- enum n, x <- trees n, y <- trees i]
    ++ [App x y | x <- trees n, y <- trees n]

terms :: [Term]
terms = concatMap (wire Zero) (concatMap trees (iterate Succ Zero))
