import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Home, Search, ArrowLeft, BookOpen, Award } from "lucide-react";

export default function ErrorNotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex flex-col">
      {/* Header */}
      <header className="px-6 py-4">
        <div className="max-w-4xl mx-auto">
          <Badge variant="secondary" className="inline-flex items-center gap-2">
            🚀 AI Skills Verification Platform
          </Badge>
        </div>
      </header>

      {/* Main 404 Content */}
      <main className="flex-1 flex items-center justify-center px-6 py-20">
        <div className="max-w-2xl mx-auto text-center">
          {/* Large 404 Number */}
          <div className="mb-8">
            <h1 className="text-9xl lg:text-[12rem] bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent opacity-20 select-none">
              404
            </h1>
            <div className="-mt-16 lg:-mt-24">
              <h2 className="text-4xl lg:text-5xl bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
                Page Not Found
              </h2>
              <p className="text-xl text-muted-foreground mb-8 max-w-lg mx-auto">
                Oops! The page you're looking for seems to have gone off the blockchain. Let's get you back on track.
              </p>
            </div>
          </div>

          {/* Action Cards */}
          <div className="grid sm:grid-cols-2 gap-4 mb-12">
            <Card className="text-center border-2 hover:shadow-lg transition-all hover:scale-105">
              <CardHeader className="pb-3">
                <div className="mx-auto w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-3">
                  <Home className="h-6 w-6 text-blue-600" />
                </div>
                <CardTitle className="text-lg">Go Home</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="mb-4">
                  Return to our main page and explore skill verification
                </CardDescription>
                <Button className="w-full">
                  <Home className="mr-2 h-4 w-4" />
                  Back to Home
                </Button>
              </CardContent>
            </Card>

            <Card className="text-center border-2 hover:shadow-lg transition-all hover:scale-105">
              <CardHeader className="pb-3">
                <div className="mx-auto w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-3">
                  <BookOpen className="h-6 w-6 text-purple-600" />
                </div>
                <CardTitle className="text-lg">Browse Tests</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="mb-4">
                  Discover available skill tests and start learning
                </CardDescription>
                <Button variant="outline" className="w-full">
                  <BookOpen className="mr-2 h-4 w-4" />
                  View Tests
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Quick Links */}
          <div className="mb-8">
            <p className="text-muted-foreground mb-4">Or try these popular pages:</p>
            <div className="flex flex-wrap justify-center gap-3">
              <Button variant="ghost" size="sm">
                <Search className="mr-2 h-4 w-4" />
                Search Tests
              </Button>
              <Button variant="ghost" size="sm">
                <Award className="mr-2 h-4 w-4" />
                Verify Credential
              </Button>
              <Button variant="ghost" size="sm">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Go Back
              </Button>
            </div>
          </div>

          {/* Help Text */}
          <Card className="bg-white/50 border-dashed">
            <CardContent className="pt-6">
              <p className="text-sm text-muted-foreground">
                Still having trouble? The page you're looking for might have been moved, deleted, or you might have typed the URL incorrectly. 
                If you believe this is an error, please contact our support team.
              </p>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Footer */}
      <footer className="px-6 py-8 bg-white/30">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-sm text-muted-foreground">
            © 2025 AI Skills Verification Platform. Built with ❤️ for the future of education.
          </p>
        </div>
      </footer>
    </div>
  );
}