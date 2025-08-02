import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { 
  Trophy, 
  Clock, 
  Play, 
  Eye, 
  RotateCcw, 
  TrendingUp, 
  Calendar,
  Award,
  CheckCircle,
  AlertCircle,
  Code,
  FileText,
  Zap
} from "lucide-react";

// Mock user data
const userData = {
  name: "Damola",
  email: "damola@example.com",
  joinDate: "January 2025",
  totalTests: 12,
  passedTests: 8,
  averageScore: 87,
  streak: 5
};

// Mock test data with different statuses
const mockTests = [
  {
    id: "python-basics",
    title: "Intro to Python",
    description: "Master Python fundamentals including variables, data types, and control structures",
    category: "Programming",
    difficulty: "Beginner",
    duration: 45,
    totalQuestions: 15,
    status: "not_started",
    icon: Code,
    color: "blue"
  },
  {
    id: "javascript-advanced",
    title: "Advanced JavaScript",
    description: "Deep dive into closures, async programming, and modern ES6+ features",
    category: "Programming", 
    difficulty: "Advanced",
    duration: 60,
    totalQuestions: 20,
    status: "submitted",
    score: 85,
    submittedAt: "2 hours ago",
    icon: Code,
    color: "yellow"
  },
  {
    id: "react-fundamentals",
    title: "React Fundamentals",
    description: "Learn React components, state management, and hooks",
    category: "Frontend",
    difficulty: "Intermediate",
    duration: 50,
    totalQuestions: 18,
    status: "passed",
    score: 92,
    completedAt: "3 days ago",
    credentialId: "0x1234...abcd",
    icon: Code,
    color: "green"
  },
  {
    id: "data-structures",
    title: "Data Structures & Algorithms",
    description: "Understanding arrays, linked lists, trees, and sorting algorithms",
    category: "Computer Science",
    difficulty: "Intermediate",
    duration: 75,
    totalQuestions: 25,
    status: "failed",
    score: 45,
    completedAt: "1 week ago",
    canRetake: true,
    icon: FileText,
    color: "red"
  },
  {
    id: "web-security",
    title: "Web Security Basics",
    description: "Learn about HTTPS, authentication, and common security vulnerabilities",
    category: "Security",
    difficulty: "Beginner",
    duration: 40,
    totalQuestions: 12,
    status: "not_started",
    icon: FileText,
    color: "purple"
  }
];

const recentActivity = [
  { action: "Passed React Fundamentals test", time: "3 days ago", score: 92 },
  { action: "Started Advanced JavaScript test", time: "5 days ago", score: null },
  { action: "Earned Python Basics credential", time: "1 week ago", score: 88 },
  { action: "Retook Data Structures test", time: "2 weeks ago", score: 45 }
];

export default function UserDashboard() {
  const getStatusBadge = (test: typeof mockTests[0]) => {
    switch (test.status) {
      case "not_started":
        return <Badge variant="secondary">Not Started</Badge>;
      case "submitted":
        return <Badge variant="outline" className="border-yellow-500 text-yellow-700">Under Review</Badge>;
      case "passed":
        return <Badge variant="default" className="bg-green-600">Passed</Badge>;
      case "failed":
        return <Badge variant="destructive">Failed</Badge>;
      default:
        return null;
    }
  };

  const getActionButton = (test: typeof mockTests[0]) => {
    switch (test.status) {
      case "not_started":
        return (
          <Button className="w-full">
            <Play className="mr-2 h-4 w-4" />
            Take Test
          </Button>
        );
      case "submitted":
        return (
          <Button variant="outline" className="w-full" disabled>
            <Clock className="mr-2 h-4 w-4" />
            Grading in Progress
          </Button>
        );
      case "passed":
        return (
          <div className="space-y-2">
            <Button variant="outline" className="w-full">
              <Eye className="mr-2 h-4 w-4" />
              View Results
            </Button>
            <Button className="w-full">
              <Award className="mr-2 h-4 w-4" />
              View Credential NFT
            </Button>
          </div>
        );
      case "failed":
        return (
          <div className="space-y-2">
            <Button variant="outline" className="w-full">
              <Eye className="mr-2 h-4 w-4" />
              View Results
            </Button>
            {test.canRetake && (
              <Button className="w-full">
                <RotateCcw className="mr-2 h-4 w-4" />
                Retake Test
              </Button>
            )}
          </div>
        );
      default:
        return null;
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "Beginner":
        return "bg-green-100 text-green-700";
      case "Intermediate":
        return "bg-yellow-100 text-yellow-700";
      case "Advanced":
        return "bg-red-100 text-red-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="px-6 py-6 bg-white/80 backdrop-blur-sm border-b">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between">
            <Badge variant="secondary" className="inline-flex items-center gap-2">
              🚀 AI Skills Verification Platform
            </Badge>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-muted-foreground">Welcome back,</p>
                <p className="font-medium">{userData.name}</p>
              </div>
              <Avatar>
                <AvatarImage src="/placeholder-avatar.jpg" alt={userData.name} />
                <AvatarFallback className="bg-gradient-to-r from-blue-500 to-purple-500 text-white">
                  {userData.name.charAt(0)}
                </AvatarFallback>
              </Avatar>
            </div>
          </div>
        </div>
      </header>

      <main className="px-6 py-8">
        <div className="max-w-7xl mx-auto space-y-8">
          {/* Welcome Section */}
          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <Card className="border-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white">
                <CardHeader>
                  <CardTitle className="text-2xl">Hi {userData.name}! 👋</CardTitle>
                  <CardDescription className="text-blue-100">
                    Ready to continue your skill verification journey?
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white/20 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-1">
                        <Trophy className="h-5 w-5" />
                        <span className="text-sm">Tests Passed</span>
                      </div>
                      <p className="text-2xl font-bold">{userData.passedTests}/{userData.totalTests}</p>
                    </div>
                    <div className="bg-white/20 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-1">
                        <TrendingUp className="h-5 w-5" />
                        <span className="text-sm">Average Score</span>
                      </div>
                      <p className="text-2xl font-bold">{userData.averageScore}%</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="space-y-4">
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-lg">Quick Stats</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Current Streak</span>
                    <div className="flex items-center gap-1">
                      <Zap className="h-4 w-4 text-yellow-500" />
                      <span className="font-medium">{userData.streak} days</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Member Since</span>
                    <span className="font-medium">{userData.joinDate}</span>
                  </div>
                  <div className="pt-2">
                    <div className="flex justify-between text-sm mb-2">
                      <span>Progress to Next Level</span>
                      <span>75%</span>
                    </div>
                    <Progress value={75} className="h-2" />
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Available Tests */}
          <div>
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-medium">Available Tests</h2>
                <p className="text-muted-foreground">Choose a test to verify your skills</p>
              </div>
              <Button variant="outline">
                <Calendar className="mr-2 h-4 w-4" />
                View All Tests
              </Button>
            </div>

            <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {mockTests.map((test) => {
                const IconComponent = test.icon;
                return (
                  <Card key={test.id} className="border-2 hover:shadow-lg transition-all">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                          <div className={`w-10 h-10 rounded-lg bg-${test.color}-100 flex items-center justify-center`}>
                            <IconComponent className={`h-5 w-5 text-${test.color}-600`} />
                          </div>
                          <div>
                            <CardTitle className="text-lg">{test.title}</CardTitle>
                            <div className="flex items-center gap-2 mt-1">
                              <Badge variant="outline" className={getDifficultyColor(test.difficulty)}>
                                {test.difficulty}
                              </Badge>
                              {getStatusBadge(test)}
                            </div>
                          </div>
                        </div>
                      </div>
                      <CardDescription className="mt-2">
                        {test.description}
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="flex items-center justify-between text-sm text-muted-foreground">
                        <span>{test.duration} minutes</span>
                        <span>{test.totalQuestions} questions</span>
                        <span>{test.category}</span>
                      </div>

                      {test.score && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-muted-foreground">Score:</span>
                          <span className={`font-medium ${test.score >= 70 ? 'text-green-600' : 'text-red-600'}`}>
                            {test.score}%
                          </span>
                        </div>
                      )}

                      {test.submittedAt && (
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <Clock className="h-4 w-4" />
                          <span>Submitted {test.submittedAt}</span>
                        </div>
                      )}

                      {test.completedAt && (
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <Calendar className="h-4 w-4" />
                          <span>Completed {test.completedAt}</span>
                        </div>
                      )}

                      {test.credentialId && (
                        <div className="flex items-center gap-2 text-sm text-green-600">
                          <CheckCircle className="h-4 w-4" />
                          <span>NFT Credential Minted</span>
                        </div>
                      )}

                      <div className="pt-2">
                        {getActionButton(test)}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>

          {/* Recent Activity */}
          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                  <CardDescription>Your latest test activities and achievements</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentActivity.map((activity, index) => (
                      <div key={index} className="flex items-center gap-4 p-3 rounded-lg hover:bg-muted/50 transition-colors">
                        <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                          {activity.score ? (
                            activity.score >= 70 ? (
                              <CheckCircle className="h-4 w-4 text-green-600" />
                            ) : (
                              <AlertCircle className="h-4 w-4 text-red-600" />
                            )
                          ) : (
                            <Clock className="h-4 w-4 text-blue-600" />
                          )}
                        </div>
                        <div className="flex-1">
                          <p className="text-sm font-medium">{activity.action}</p>
                          <p className="text-xs text-muted-foreground">{activity.time}</p>
                        </div>
                        {activity.score && (
                          <Badge variant={activity.score >= 70 ? "default" : "destructive"} className="text-xs">
                            {activity.score}%
                          </Badge>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            <div>
              <Card>
                <CardHeader>
                  <CardTitle>Achievement Badges</CardTitle>
                  <CardDescription>Your earned credentials</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="text-center p-3 rounded-lg border bg-green-50">
                      <Award className="h-8 w-8 text-green-600 mx-auto mb-2" />
                      <p className="text-xs font-medium">First Test</p>
                    </div>
                    <div className="text-center p-3 rounded-lg border bg-blue-50">
                      <Trophy className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                      <p className="text-xs font-medium">High Scorer</p>
                    </div>
                    <div className="text-center p-3 rounded-lg border bg-purple-50">
                      <Zap className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                      <p className="text-xs font-medium">5 Day Streak</p>
                    </div>
                    <div className="text-center p-3 rounded-lg border-dashed border-gray-300">
                      <div className="h-8 w-8 rounded-full bg-gray-200 mx-auto mb-2"></div>
                      <p className="text-xs text-muted-foreground">Locked</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}