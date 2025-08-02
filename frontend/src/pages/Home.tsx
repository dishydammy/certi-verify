import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle, Cpu, FileCheck, Zap, Shield, Award } from "lucide-react";
// import { ImageWithFallback } from "./components/figma/ImageWithFallback";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Hero Section */}
      <section className="relative px-6 py-20 text-center">
        <div className="max-w-4xl mx-auto">
          <div className="mb-6">
            <Badge variant="secondary" className="mb-4">
              🚀 Powered by AI + Blockchain
            </Badge>
          </div>
          
          <h1 className="mb-6 text-5xl lg:text-6xl bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Verify Skills. Instantly. Authentically.
          </h1>
          
          <p className="mb-8 text-xl text-muted-foreground max-w-2xl mx-auto">
            AI-graded tests with blockchain-verified certificates. Take a test and mint your proof of knowledge.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="text-lg px-8 py-6">
              <Zap className="mr-2 h-5 w-5" />
              Take a Test
            </Button>
            <Button variant="outline" size="lg" className="text-lg px-8 py-6">
              <Shield className="mr-2 h-5 w-5" />
              Verify Credential
            </Button>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="px-6 py-16 bg-white/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="mb-4 text-3xl">How It Works</h2>
            <p className="text-muted-foreground text-lg">
              Three simple steps to earn your verified skill credential
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="text-center border-2 hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                  <FileCheck className="h-8 w-8 text-blue-600" />
                </div>
                <CardTitle className="flex items-center justify-center gap-2">
                  <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm">1</span>
                  Take a Skill Test
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Answer MCQs, coding challenges, and short questions designed to test your knowledge.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center border-2 hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                  <Cpu className="h-8 w-8 text-purple-600" />
                </div>
                <CardTitle className="flex items-center justify-center gap-2">
                  <span className="bg-purple-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm">2</span>
                  Get Instant Grading
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Our AI grades your answers instantly and provides detailed feedback on your performance.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center border-2 hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
                  <Award className="h-8 w-8 text-green-600" />
                </div>
                <CardTitle className="flex items-center justify-center gap-2">
                  <span className="bg-green-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm">3</span>
                  Earn Blockchain Credential
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Pass the test and we'll mint a verified NFT certificate on-chain as proof of your skills.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Showcase Credential Section */}
      <section className="px-6 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="mb-4 text-3xl">Sample Blockchain Credential</h2>
          <p className="mb-12 text-muted-foreground text-lg">
            Here's what your verified skill certificate looks like
          </p>
          
          <div className="max-w-md mx-auto">
            <Card className="border-2 border-gradient-to-r from-blue-500 to-purple-500 shadow-xl">
              <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-t-lg">
                <div className="flex items-center justify-between">
                  <Badge variant="secondary" className="bg-white/20 text-white border-white/20">
                    NFT Certificate
                  </Badge>
                  <CheckCircle className="h-6 w-6" />
                </div>
                <CardTitle className="text-xl">Intro to Python</CardTitle>
                <CardDescription className="text-blue-100">
                  Blockchain-Verified Skill Certificate
                </CardDescription>
              </CardHeader>
              <CardContent className="p-6">
                <div className="space-y-3 text-left">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Student ID:</span>
                    <span>ST-2025-001234</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Score:</span>
                    <span className="text-green-600">92/100</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Date:</span>
                    <span>Aug 1, 2025</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Blockchain:</span>
                    <span className="text-blue-600">Polygon Mumbai</span>
                  </div>
                </div>
                <Button variant="outline" className="w-full mt-6">
                  View on Polygon Mumbai
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="px-6 py-16 bg-white/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="mb-8 text-3xl">Powered by Cutting-Edge Technology</h2>
          <div className="flex flex-wrap justify-center gap-4">
            <Badge variant="outline" className="px-4 py-2 text-sm">
              GPT AI
            </Badge>
            <Badge variant="outline" className="px-4 py-2 text-sm">
              Solidity Smart Contracts
            </Badge>
            <Badge variant="outline" className="px-4 py-2 text-sm">
              Ethers.js
            </Badge>
            <Badge variant="outline" className="px-4 py-2 text-sm">
              Polygon Network
            </Badge>
            <Badge variant="outline" className="px-4 py-2 text-sm">
              IPFS Storage
            </Badge>
            <Badge variant="outline" className="px-4 py-2 text-sm">
              React
            </Badge>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-center">
        <div className="max-w-3xl mx-auto">
          <h2 className="mb-4 text-3xl">Ready to Verify Your Skills?</h2>
          <p className="mb-8 text-xl opacity-90">
            Join the future of credential verification. Take your first test today.
          </p>
          <Button size="lg" variant="secondary" className="text-lg px-8 py-6">
            <Award className="mr-2 h-5 w-5" />
            Start Your First Test
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-12 bg-gray-900 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <div className="mb-8">
            <h3 className="mb-4 text-xl">Built for Innovation Hackathon</h3>
            <p className="text-gray-400 mb-6">
              Combining AI-powered grading with blockchain verification for the future of skill assessment.
            </p>
            <Button variant="outline" className="text-white border-white hover:bg-white hover:text-gray-900">
              View on GitHub
            </Button>
          </div>
          
          <div className="border-t border-gray-700 pt-8">
            <p className="text-gray-400">
              © 2025 AI Skills Verification Platform. Built with ❤️ for the future of education.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}