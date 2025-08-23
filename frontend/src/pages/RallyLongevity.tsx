import { useState } from "react";
import {
  Title,
  Text,
  Container,
  Stack,
  Button,
  Group,
  FileInput,
  RingProgress,
} from "@mantine/core";

const RallyLongevity = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleSubmit = async () => {
    if (!file) return;

    setUploading(true);

    try {
    } catch (error) {
      console.error("Error uploading video:", error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Container size="md" py="xl">
      <Stack gap="lg">
        <Title order={2} ta="center">
          Rally Longevity
        </Title>
        <Text ta="center" c="dimmed">
          Upload a video of your rallies and receive feedback on your
          consistency and stamina. Our AI will track how many consecutive hits
          you make.
        </Text>

        {!results ? (
          <>
            <FileInput
              label="Upload your practice video"
              placeholder="Click to select a video file"
              accept="video/*"
              value={file}
              onChange={setFile}
              size="md"
            />

            <Button
              onClick={handleSubmit}
              disabled={!file || uploading}
              loading={uploading}
              fullWidth
            >
              Analyze My Rallies
            </Button>
          </>
        ) : (
          <Stack
            gap="md"
            p="md"
            style={{ border: "1px solid #eaeaea", borderRadius: "8px" }}
          >
            <Title order={3}>Analysis Results</Title>
            <Group align="center" justify="center">
              <Stack align="center">
                <RingProgress
                  size={150}
                  thickness={12}
                  roundCaps
                  sections={[{ value: 100, color: "blue" }]}
                  label={
                    <Text ta="center" fw={700} size="xl">
                      {results.longest_rally}
                    </Text>
                  }
                />
                <Text fw={500}>Longest Rally</Text>
              </Stack>
            </Group>
            <Group>
              <Text fw={500}>Total hits:</Text>
              <Text>{results.total_hits}</Text>
            </Group>
            <Group>
              <Text fw={500}>Average rally length:</Text>
              <Text>{results.average_rally} hits</Text>
            </Group>
            <Stack gap="xs">
              <Text fw={500}>Rally breakdown:</Text>
              {results.rallies.map(
                (rally: { length: number; timestamp: string }, i: number) => (
                  <Group key={i}>
                    <Text>Rally {i + 1}:</Text>
                    <Text>
                      {rally.length} hits (at {rally.timestamp})
                    </Text>
                  </Group>
                )
              )}
            </Stack>
            <Group>
              <Text fw={500}>Feedback:</Text>
              <Text>{results.feedback}</Text>
            </Group>
            <Button onClick={() => setResults(null)} variant="outline">
              Upload Another Video
            </Button>
          </Stack>
        )}
      </Stack>
    </Container>
  );
};

export default RallyLongevity;
