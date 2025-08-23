import {
  Title,
  Text,
  Container,
  Button,
  Group,
  Stack,
  Card,
  SimpleGrid,
} from "@mantine/core";
import { useNavigate } from "react-router-dom";
import { FiActivity, FiAward, FiBarChart2, FiRepeat } from "react-icons/fi";

const features = [
  {
    title: "Forehand Practice",
    description:
      "Focus on your forehand technique with AI-powered stroke detection and feedback.",
    icon: <FiActivity size={24} />,
    path: "/practice/forehand",
  },
  {
    title: "Backhand Practice",
    description:
      "Improve your backhand with real-time tracking and analysis of your technique.",
    icon: <FiBarChart2 size={24} />,
    path: "/practice/backhand",
  },
  {
    title: "Alternation Challenge",
    description:
      "Master the art of switching between forehand and backhand strokes seamlessly.",
    icon: <FiRepeat size={24} />,
    path: "/practice/alternation",
  },
  {
    title: "Rally Longevity",
    description:
      "Track and improve your rally consistency and stamina with streak counting.",
    icon: <FiAward size={24} />,
    path: "/practice/rally",
  },
];

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <Container size="xl" py="xl">
      <Stack gap="xl" align="center" mb={50}>
        <Title order={1} ta="center" mb="md">
          Level Up Your Table Tennis Skills
        </Title>
        <Text size="lg" ta="center" mb="xl" c="dimmed" maw={600}>
          Upload videos of your practice sessions and get AI-powered feedback to
          improve your technique. Choose a specific skill to focus on and track
          your progress over time.
        </Text>
        <Button size="lg" onClick={() => navigate("/practice/forehand")}>
          Get Started
        </Button>
      </Stack>

      {/* How It Works */}
      <Stack gap="xl" mb={50}>
        <Title order={2} ta="center" mb="xl">
          How It Works
        </Title>
        <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="md">
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Text fw={500} size="lg" mb="xs">
              1. Choose Your Practice Mode
            </Text>
            <Text c="dimmed">
              Select what skill you want to focus on: forehand, backhand,
              alternation, or rally longevity.
            </Text>
          </Card>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Text fw={500} size="lg" mb="xs">
              2. Upload Your Video
            </Text>
            <Text c="dimmed">
              Record yourself practicing and upload the video to our system.
            </Text>
          </Card>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Text fw={500} size="lg" mb="xs">
              3. AI Analysis
            </Text>
            <Text c="dimmed">
              Our machine learning models analyze your strokes, movements, and
              technique.
            </Text>
          </Card>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Text fw={500} size="lg" mb="xs">
              4. Get Personalized Feedback
            </Text>
            <Text c="dimmed">
              Receive detailed statistics and suggestions to improve your game.
            </Text>
          </Card>
        </SimpleGrid>
      </Stack>

      {/* Practice Modes */}
      <Stack gap="xl" mb={50}>
        <Title order={2} ta="center" mb="xl">
          Practice Modes
        </Title>
        <SimpleGrid cols={{ base: 1, sm: 2, md: 4 }} spacing="md">
          {features.map((feature) => (
            <Card
              shadow="sm"
              padding="lg"
              radius="md"
              withBorder
              key={feature.title}
            >
              <Group mb="md">
                {feature.icon}
                <Text fw={500}>{feature.title}</Text>
              </Group>
              <Text size="sm" c="dimmed" mb="xl">
                {feature.description}
              </Text>
              <Button
                variant="light"
                fullWidth
                onClick={() => navigate(feature.path)}
              >
                Select
              </Button>
            </Card>
          ))}
        </SimpleGrid>
      </Stack>

      {/* Call to Action */}
      <Stack align="center" mt={50}>
        <Title order={3} ta="center" mb="md">
          Ready to improve your table tennis skills?
        </Title>
        <Button size="lg" onClick={() => navigate("/practice/forehand")}>
          Start Practicing Now
        </Button>
      </Stack>
    </Container>
  );
};

export default HomePage;
