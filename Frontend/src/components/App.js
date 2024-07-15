import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import SignUp from "./SignUp";
import Login from "./Login";
import NavBar from "./NavBar";
import Home from "./Home";
import Footer from "./Footer";
import Transactions from "./Transactions";
import Loans from "./Loans";
import Subscriptions from "./Subscriptions";
import Savings from "./Savings";
import DashNavBar from "./DashNavBar";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/check_session").then((r) => {
      if (r.ok && r.status !== 200) {
        setLoading(false);
      } else {
        r.json().then((user) => {
          debugger
          setUser(user);
        });
        setLoading(false);
      }
    });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <NavBar user={user} setUser={setUser} />
      <main>
        {user ? (
          <>
            <DashNavBar /> {/* Keep DashNavBar visible for logged-in users */}
            <Switch>
              <Route path="/" exact>
                <Home user={user} />
              </Route>
              <Route path="/transactions">
                <Transactions user={user} />
              </Route>
              <Route path="/loans">
                <Loans user={user} />
              </Route>
              <Route path="/subscriptions">
                <Subscriptions user={user} />
              </Route>
              <Route path="/savings">
                <Savings user={user} />
              </Route>
            </Switch>
          </>
        ) : (
          <Switch>
            <Route path="/signup">
              <SignUp setUser={setUser} />
            </Route>
            <Route path="/login">
              <Login setUser={setUser} />
            </Route>
            <Route path="/" exact>
              <Home />
            </Route>
          </Switch>
        )}
      </main>
      <Footer />
    </>
  );
}

export default App;
